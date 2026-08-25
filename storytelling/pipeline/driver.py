#!/usr/bin/env python3
"""
3-stage episode-writing pipeline driver (plan -> prose -> JSON format)
with mechanical validation gates and a reader-comprehension probe.

Stdlib + urllib only. Does NOT hand-edit generated content; it only
re-prompts stages with deficiency notes.

Usage:
  python3 driver.py --ep-id ep_002 --foreground char_sangwan \
      --places place_letter_writers_landing,place_pawnshop \
      --tags tag_254,tag_083,tag_167,tag_154,tag_337,tag_120,tag_197,tag_041 \
      --model-plan MODEL --model-prose MODEL --model-format MODEL \
      --out /path/out.json --report /path/report.md
"""

import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

WORLD_DIR = "/mnt/agents/output/world"
REPO_PUBLIC = "/mnt/agents/thai-rpg-content/public"
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(PIPELINE_DIR, "prompts")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# $ per 1M tokens: {"model": (prompt, completion)} — extend/override as needed.
MODEL_PRICES = {
    "moonshotai/kimi-k2.5": (0.6, 3.0),
    "deepseek/deepseek-v3.2": (0.26, 0.38),
    "qwen/qwen3-235b-a22b-2507": (0.09, 0.55),
    "default": (1.0, 5.0),
}

MAX_TRIES = 3          # per-stage re-prompts
MAX_RESTARTS = 2       # full plan->probe restarts after probe FAIL

log_lines = []  # report buffer


def log(msg):
    print(msg, flush=True)
    log_lines.append(msg)


# ---------------------------------------------------------------- API calls
class Usage:
    def __init__(self):
        self.prompt = 0
        self.completion = 0
        self.cost = 0.0

    def add(self, model, usage):
        p = usage.get("prompt_tokens", 0) or 0
        c = usage.get("completion_tokens", 0) or 0
        self.prompt += p
        self.completion += c
        pp, cp = MODEL_PRICES.get(model, MODEL_PRICES["default"])
        self.cost += (p * pp + c * cp) / 1_000_000.0
        return p, c


def call_llm(model, system, user, temperature, max_tokens, usage, label):
    """One OpenRouter chat completion. Returns (text, finish_reason)."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY env var is not set")
    # Split "SYSTEM:"/"USER:" convention used in the prompt templates.
    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost/thai-rpg-pipeline",
            "X-Title": "thai-rpg-episode-pipeline",
        },
    )
    max_api_attempts = 8
    for attempt in range(max_api_attempts):
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                raw = resp.read().decode("utf-8", "replace")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                # some upstream providers emit raw control chars inside strings
                try:
                    data = json.loads(raw, strict=False)
                except json.JSONDecodeError as je:
                    log(f"[api] {label}: truncated/invalid JSON body "
                        f"(len={len(raw)}): ...{raw[max(0, je.pos-80):je.pos+80]!r}")
                    raise
            if "error" in data:
                raise RuntimeError(f"API error payload: {data['error']}")
            _msg = data["choices"][0]["message"].get("content")
            _fr = data["choices"][0].get("finish_reason")
            if not _msg or _fr == "length":
                log(f"[api] {label}: empty content or length-truncated (finish={_fr}, attempt {attempt+1}/{max_api_attempts})")
                if attempt == max_api_attempts - 1:
                    raise RuntimeError(f"{label}: model kept returning empty/truncated content")
                time.sleep(5)
                continue
            break
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:500]
            log(f"[api] {label}: HTTP {e.code} (attempt {attempt+1}/{max_api_attempts}): {body}")
            if attempt == max_api_attempts - 1:
                raise
            time.sleep(min(120, 10 * (attempt + 1)))
        except Exception as e:
            log(f"[api] {label}: {type(e).__name__}: {e} (attempt {attempt+1}/{max_api_attempts})")
            if attempt == max_api_attempts - 1:
                raise
            time.sleep(min(120, 10 * (attempt + 1)))
    msg = data["choices"][0]["message"]["content"]
    p, c = usage.add(model, data.get("usage", {}))
    log(f"[api] {label}: model={model} tokens in={p} out={c}")
    return msg, data["choices"][0].get("finish_reason")


# ---------------------------------------------------------------- file input
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_world_file(prefix_id):
    """char_x / place_x -> prefer <id>.md, then <id>_private.md, then <id>.json."""
    for cand in (f"{prefix_id}.md", f"{prefix_id}_private.md", f"{prefix_id}.json"):
        p = os.path.join(WORLD_DIR, cand)
        if os.path.exists(p):
            return read_file(p)
    return None


def load_character_text(char_id):
    text = find_world_file(char_id)
    if text is not None:
        return f"### {char_id}\n{text}"
    chars = load_json(os.path.join(REPO_PUBLIC, "characters.json"))
    for c in chars:
        if c.get("id") == char_id:
            return f"### {char_id} ({c.get('name','')})\n{c.get('description','')}"
    log(f"[warn] no data found for character {char_id}")
    return f"### {char_id}\n(no file found)"


def load_place_text(place_id):
    text = find_world_file(place_id)
    if text is not None:
        return f"### {place_id}\n{text}"
    places = load_json(os.path.join(REPO_PUBLIC, "places.json"))
    for p in places:
        if p.get("id") == place_id:
            return f"### {place_id} ({p.get('name','')})\n{p.get('description','')}"
    log(f"[warn] no data found for place {place_id}")
    return f"### {place_id}\n(no file found)"


def assign_anchors(tag_ids):
    """Pick one anchor vocab item per tag, deterministically (first item with 1-6 Thai words)."""
    tags = load_json(os.path.join(REPO_PUBLIC, "tags.json"))
    vocab = load_json(os.path.join(REPO_PUBLIC, "vocab_items.json"))
    by_id = {t["id"]: t for t in tags}
    anchors = {}
    for tid in tag_ids:
        t = by_id[tid]
        cands = [v for v in vocab if v["id"] in set(t["vocab_item_ids"])]
        pick = None
        for v in cands:
            thai = re.sub(r"\([^)]*\)", "", v["thai"]).strip()  # strip optional parens
            thai = thai.split(" / ")[0].strip()  # take first alternative
            if 1 <= len(thai.split()) <= 6 and len(re.sub(r"[^\u0e00-\u0e7f]", "", thai)) >= 4:
                pick = (thai, v["english"]); break
        if pick is None and cands:
            v = cands[0]
            pick = (re.sub(r"\([^)]*\)", "", v["thai"]).strip(), v["english"])
        anchors[tid] = pick
    return anchors


def resolve_tags(tag_ids):
    tags = load_json(os.path.join(REPO_PUBLIC, "tags.json"))
    by_id = {t["id"]: t for t in tags}
    out = []
    for tid in tag_ids:
        t = by_id.get(tid)
        if t is None:
            raise SystemExit(f"unknown tag id: {tid}")
        vocab = load_json(os.path.join(REPO_PUBLIC, "vocab_items.json"))
        items = [v for v in vocab if v["id"] in set(t["vocab_item_ids"])]
        lines = "\n".join(f'    - {v["thai"]} = {v["english"]}' for v in items)
        out.append(f"{tid} — {t['name']}\n  Choose this tag's Thai anchor phrase VERBATIM from these vocab items:\n{lines}")
    return "\n".join(out)


def fill(template, slots):
    out = template
    for k, v in slots.items():
        out = out.replace("{{%s}}" % k, v)
    return out


def split_sys_user(template_text):
    """Templates start with 'SYSTEM:' ... 'USER:' sections."""
    m = re.search(r"^USER:\s*$", template_text, re.M)
    if m:
        return template_text[:m.start()].replace("SYSTEM:", "", 1).strip(), template_text[m.end():].strip()
    return "You are a helpful assistant.", template_text


# ---------------------------------------------------------------- stage gates
SECTION_NAMES = [
    "STICKY SITUATION", "WHY IT MATTERS", "CENTRAL OBJECT", "ACT MAP",
    "READER QUESTIONS", "SECRET HANDLING", "TAG PLAN",
]


def check_plan(plan, foreground):
    problems = []
    for name in SECTION_NAMES:
        if not re.search(rf"^#{{1,4}}\s+{re.escape(name)}\b", plan, re.M):
            problems.append(f"missing mandatory section header: '{name}'")
    m = re.search(r"^#{1,4}\s+WHY IT MATTERS\b(.*?)(?=^#{1,4}\s|\Z)", plan, re.M | re.S)
    if m:
        body = m.group(1).lower()
        if "pricha" not in body:
            problems.append("WHY IT MATTERS has no entry for the PC Pricha")
        fg_name = foreground.replace("char_", "").lower()
        if fg_name not in body and foreground not in body:
            problems.append(f"WHY IT MATTERS has no entry for the foregrounded character ({foreground})")
    m = re.search(r"^#{1,4}\s+CENTRAL OBJECT\b(.*?)(?=^#{1,4}\s|\Z)", plan, re.M | re.S)
    if m:
        if not re.search(r"own|belong|whose|hers\b|his\b|their", m.group(1), re.I):
            problems.append("CENTRAL OBJECT does not state who owns it")
    plan_scanned = re.sub(r"^#{1,4}\s+(?:SECRET HANDLING|VOCABULARY[^\n]*|COMPLIANCE[^\n]*)\b.*?(?=^#{1,4}\s|\Z)", "", plan, flags=re.M | re.S | re.I)
    # strip short quoted spans (models citing banned words) — plans contain no real dialogue
    plan_scanned = re.sub(r'[“"][^”"]{1,60}[”"]', ' ', plan_scanned)
    for bs in BANNED_SUBSTRINGS:
        if bs.lower() in plan_scanned.lower():
            i = plan.lower().find(bs.lower())
            i = plan_scanned.lower().find(bs.lower())
            problems.append(f"plan contains banned string {bs!r}: ...{plan_scanned[max(0,i-40):i+40]!r}...")
    for rx, label in BANNED_REGEXES:
        m2 = rx.search(plan_scanned)
        if m2:
            problems.append(f"plan contains banned pattern {label}: ...{plan_scanned[max(0,m2.start()-40):m2.end()+40]!r}...")
    return problems


BANNED_SUBSTRINGS = ["No. Only"]
BANNED_REGEXES = [
    (re.compile(r"\bforg(ery|ed|e|es|ing)\b", re.I), "forgery-language"),
    (re.compile(r"\bdead\b|\bdied\b|\bdeath\b|\bghost", re.I), "death-language"),
    (re.compile(r"\bthe late\s+[A-Z]"), "'the late X' (implies death)"),
        (re.compile(r"\bor\s+\w+[.?!]?\s+or\s+both", re.I), "'Or X. Or both.' fragment"),
    (re.compile(r"(?:^|(?<=[.!?]\s))Not [A-Z]"), "sentence-opener 'Not X'"),
]


def extract_anchor_phrases(plan):
    """Pull Thai-script anchor phrases out of the plan's TAG PLAN section."""
    m = re.search(r"^#{1,4}\s+TAG PLAN\b(.*?)(?=^#{1,4}\s|\Z)", plan, re.M | re.S)
    text = m.group(1) if m else plan
    phrases = []
    for line in text.splitlines():  # never let a phrase span lines
        phrases.extend(re.findall(r"[\u0e00-\u0e7f][\u0e00-\u0e7f \t]*[\u0e00-\u0e7f]", line))
    # normalize whitespace, dedupe, keep order
    seen, out = set(), []
    for p in phrases:
        p = re.sub(r"\s+", " ", p).strip(" —-–")
        if p and len(p.split()) > 4:
            continue  # anchors are short classroom phrases, not clauses
        letters = re.sub(r"[^\u0e00-\u0e7f]", "", p)
        if len(letters) < 4 or p in {"ครับ", "ค่ะ", "คะ", "นะ", "จ้ะ"}:
            continue  # too short / bare particle
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def check_prose(prose, plan, assigned=None):
    problems = []
    for s in BANNED_SUBSTRINGS:
        # word-boundary at the start so e.g. 'died' doesn't match 'studied';
        # 'forg' still prefix-matches forgot/forgive/forgotten as intended.
        rx = re.compile(r"\b" + re.escape(s), re.I)
        mm = rx.search(prose)
        if mm:
            idx = mm.start()
            problems.append(f"banned string '{s}': ...{prose[max(0,idx-40):idx+40]!r}...")
    for rx, name in BANNED_REGEXES:
        for mm in rx.finditer(prose):
            problems.append(f"banned pattern {name}: ...{prose[max(0,mm.start()-30):mm.end()+30]!r}...")
            break
    if assigned is not None:
        anchors = [a[0] for a in assigned.values() if a]
    else:
        anchors = extract_anchor_phrases(plan)
    norm_prose = re.sub(r"\s+", " ", prose)
    missing = [p for p in anchors if p not in norm_prose]
    if missing:
        problems.append(f"missing Thai anchor phrases from the plan: {missing}")
    similes = len(re.findall(r"\bas if\b|\blike\b", prose, re.I))
    if similes > 2:
        problems.append(f"too many similes ({similes}); max 2, and only from the story's own material")
    if len(re.findall(r"^#{1,3}\s+Act\s+\d|^\*\*Act\s+\d|^Act\s+\d\s*[::—-]", prose, re.M)) != 4:
        problems.append("prose does not contain exactly four '## Act N' sections")
    return problems


# ---------------------------------------------------------------- JSON validation
SEG_PATTERN = ["narrative", "tag", "narrative", "tag", "narrative"]
ATTRIBUTES = {"attr_heart_water", "attr_deference", "attr_ledger",
              "attr_word_hoard", "attr_merit_water"}


def wc(s):
    return len(s.split())


def validate_line(line, char_ids, place_ids, where, errors):
    if not isinstance(line, dict):
        errors.append(f"{where}: line is not an object")
        return
    for key in ("character", "place", "dialogue", "stage_directions"):
        if key not in line:
            errors.append(f"{where}: line missing key '{key}'")
    if line.get("character") not in char_ids:
        errors.append(f"{where}: unknown character '{line.get('character')}'")
    if line.get("place") not in place_ids:
        errors.append(f"{where}: unknown place '{line.get('place')}'")
    if not line.get("dialogue"):
        errors.append(f"{where}: empty dialogue")


def is_first_person(s):
    return bool(re.search(r"(^|[\s'\"])(I|We|My|Mine|Me|Our|Us)\b", s)) or bool(
        re.search(r"\b(i|we|my|mine|me|our|us)\b", s))


def looks_third_person_narration(s):
    if is_first_person(s):
        return False
    # heuristic on the FIRST sentence only: third-person scene description
    # (pronoun or "The X" opener + past-tense verb), no first/second person.
    first = re.split(r"(?<=[.!?])\s", s.strip(), 1)[0]
    if "?" in first:
        return False
    third = re.search(r"\b(he|she|they|his|her|their)\b", first, re.I) or first.startswith("The ")
    second = re.search(r"\b(you|your|yours)\b", first, re.I)
    past = re.search(r"\b\w+(ed|stood|sat|held|watched|walked|looked|turned|came|went|took|gave|said)\b", first, re.I)
    return bool(third and past and not second)


def validate_episode(ep, ep_id, char_ids, place_ids, assigned_tags):
    errors = []
    if not isinstance(ep, dict):
        return ["top-level JSON is not an object"]
    if ep.get("id") != ep_id:
        errors.append(f"id is {ep.get('id')!r}, expected {ep_id!r}")
    acts = ep.get("acts")
    if not isinstance(acts, list) or len(acts) != 4:
        errors.append(f"acts must be a list of 4 (got {len(acts) if isinstance(acts, list) else type(acts).__name__})")
        # banned-language scan across all dialogue/stage_directions/descriptions
    def _walk(o):
        if isinstance(o, dict):
            for v in o.values(): yield from _walk(v)
        elif isinstance(o, list):
            for v in o: yield from _walk(v)
        elif isinstance(o, str):
            yield o
    for text in _walk(ep):
        for bs in BANNED_SUBSTRINGS:
            if bs.lower() in text.lower():
                errors.append(f"banned string {bs!r}: ...{text[max(0,text.lower().find(bs.lower())-40):text.lower().find(bs.lower())+40]!r}...")
        for rx, label in BANNED_REGEXES:
            m = rx.search(text)
            if m:
                errors.append(f"banned pattern {label}: ...{text[max(0,m.start()-40):m.end()+40]!r}...")
    return errors

    all_dialogue = []   # (text, where) for duplicate scan
    used_tags = []
    choice_descriptions = []

    for i, act in enumerate(acts):
        where = f"act {i+1}"
        if act.get("id") != f"act_{i+1}":
            errors.append(f"{where}: id is {act.get('id')!r}, expected 'act_{i+1}'")
        if not act.get("title"):
            errors.append(f"{where}: missing title")
        segs = act.get("segments")
        if not isinstance(segs, list) or len(segs) != 5:
            errors.append(f"{where}: segments must be a list of 5 "
                          f"(narrative,tag,narrative,tag,narrative); got "
                          f"{len(segs) if isinstance(segs, list) else type(segs).__name__}")
            continue
        for si, seg in enumerate(segs):
            sw = f"{where} segment {si+1}"
            expect = SEG_PATTERN[si]
            if expect == "narrative":
                if isinstance(seg, dict):
                    # tolerate {"type":"narrative","lines":[...]} wrappers
                    if seg.get("type") == "narrative" and isinstance(seg.get("lines"), list):
                        lines = seg["lines"]
                    else:
                        errors.append(f"{sw}: expected a narrative lines-array, got object {sorted(seg.keys())}")
                        continue
                elif isinstance(seg, list):
                    lines = seg
                else:
                    errors.append(f"{sw}: expected a narrative lines-array, got {type(seg).__name__}")
                    continue
                lo, hi = (4, 6) if si == 0 else (2, 3)
                if not (lo <= len(lines) <= hi):
                    errors.append(f"{sw}: has {len(lines)} lines (expected {lo}-{hi})")
                for li, line in enumerate(lines):
                    validate_line(line, char_ids, place_ids, f"{sw} line {li+1}", errors)
                    dlg = (line.get("dialogue") or "").strip()
                    all_dialogue.append((dlg, f"{sw} line {li+1}"))
                    if (line.get("character") != "char_narrator"
                            and looks_third_person_narration(dlg)):
                        errors.append(f"{sw} line {li+1}: third-person narration attributed "
                                      f"to '{line.get('character')}' (narration must be char_narrator)")
            else:  # tag
                if not (isinstance(seg, dict) and seg.get("type") == "tag"):
                    errors.append(f"{sw}: expected {{'type':'tag','tag':...}} object")
                    continue
                tid = seg.get("tag")
                used_tags.append(tid)
                if tid not in assigned_tags:
                    errors.append(f"{sw}: tag '{tid}' is not in the assigned set")

        # decision
        dec = act.get("decision")
        if not isinstance(dec, dict):
            errors.append(f"{where}: missing decision object")
            continue
        validate_line(dec.get("line", {}), char_ids, place_ids, f"{where} decision.line", errors)
        choices = dec.get("choices")
        if not isinstance(choices, list) or len(choices) != 3:
            errors.append(f"{where}: decision must have exactly 3 choices")
            continue
        diffs = sorted(c.get("difficulty", "?") for c in choices)
        if diffs != ["easy", "hard", "medium"]:
            errors.append(f"{where}: choice difficulties must be exactly easy/medium/hard (got {diffs})")
        for ci, c in enumerate(choices):
            cw = f"{where} choice {ci+1} ({c.get('difficulty','?')})"
            desc = c.get("description", "")
            choice_descriptions.append((desc, cw))
            if not (10 <= wc(desc) <= 20):
                errors.append(f"{cw}: description is {wc(desc)} words (must be 10-20)")
            if c.get("attribute") not in ATTRIBUTES:
                errors.append(f"{cw}: bad attribute '{c.get('attribute')}'")
            for kind, lo_d, hi_d in (("pass_outcome", 1, 2), ("fail_outcome", -1, 0)):
                out = c.get(kind)
                if not isinstance(out, dict):
                    errors.append(f"{cw}: missing {kind}")
                    continue
                lw = f"{cw} {kind}"
                validate_line(out.get("line", {}), char_ids, place_ids, lw, errors)
                if out.get("attribute") not in ATTRIBUTES:
                    errors.append(f"{lw}: bad attribute '{out.get('attribute')}'")
                d = out.get("delta")
                if not isinstance(d, int) or not (lo_d <= d <= hi_d):
                    errors.append(f"{lw}: delta must be in [{lo_d},{hi_d}], got {d!r}")
                oline = out.get("line", {})
                od = (oline.get("dialogue") or "").strip()
                all_dialogue.append((od, lw))
                if oline.get("character") != "char_pricha":
                    errors.append(f"{lw}: outcome line must be spoken by char_pricha (got '{oline.get('character')}')")
                if od and not od.startswith(("I ", "I'", "I’")):
                    errors.append(f"{lw}: outcome dialogue must begin with 'I ' (first person PC speech): {od[:60]!r}")
            po = ((c.get("pass_outcome") or {}).get("line") or {}).get("dialogue", "").strip()
            fo = ((c.get("fail_outcome") or {}).get("line") or {}).get("dialogue", "").strip()
            if po and fo and po == fo:
                errors.append(f"{cw}: pass_outcome and fail_outcome lines are identical")

    # duplicates
    seen = {}
    for dlg, where in all_dialogue:
        key = re.sub(r"\s+", " ", dlg.lower())
        if key and key in seen:
            errors.append(f"duplicate dialogue at {where} (first at {seen[key]}): {dlg[:60]!r}")
        else:
            seen[key] = where
    cseen = {}
    for desc, where in choice_descriptions:
        key = re.sub(r"\s+", " ", desc.lower())
        if key and key in cseen:
            errors.append(f"duplicate choice description at {where} (first at {cseen[key]})")
        else:
            cseen[key] = where

    if sorted(used_tags) != sorted(assigned_tags):
        errors.append(f"tags used {sorted(used_tags)} != assigned set {sorted(assigned_tags)}")
    return errors


# ---------------------------------------------------------------- probe
PROBE_QUESTIONS = """You are a naive reader who knows NOTHING about this story world. Read the episode JSON (character/place ids stripped of meaning) and answer four questions, numbered, in plain English:
1. What is each named character trying to get or protect, and why does the situation matter to Pricha?
2. Why does it matter to the foregrounded character (the one the story follows most closely after Pricha)?
3. The central object — whose is it, and how do you know?
4. What changes by the end?
If you cannot answer a question from the text alone, say "CANNOT TELL" for it."""

JUDGE_PROMPT = """You are a strict judge. Below are (A) the planned answers a reader should reach, from the episode plan's READER QUESTIONS section, and (B) the actual answers a naive reader gave after reading the episode with no context.

For each of the 4 planned answers, decide PASS or FAIL: PASS only if the naive reader's corresponding answer contains the planned facts. Reply in exactly this format, four lines:
Q1: PASS|FAIL — one-line reason
Q2: PASS|FAIL — one-line reason
Q3: PASS|FAIL — one-line reason
Q4: PASS|FAIL — one-line reason"""


def strip_ids(ep):
    """Deep-copy episode with character/place ids removed from text surfaces
    (keep structure; replace ids with readable placeholders)."""
    s = json.dumps(ep, ensure_ascii=False, indent=1)
    s = re.sub(r'"(character|place)":\s*"[a-z_0-9]+"', r'"\1": "…"', s)
    s = re.sub(r'"(tag|attribute|id)":\s*"[a-z_0-9]+"', r'"\1": "…"', s)
    return s


REPAIR_STAGES = {"prose"}

# ---------------------------------------------------------------- stages
def run_stage(usage, label, model, temperature, max_tokens, template_path,
              slots, checker, extra_note=""):
    """Generic generate->check->reprompt loop. Returns (text, attempts, problems)."""
    template = read_file(template_path)
    system, user = split_sys_user(fill(template, slots))
    note = ""
    for attempt in range(1, MAX_TRIES + 1):
        log(f"[{label}] attempt {attempt}/{MAX_TRIES}")
        text, _ = call_llm(model, system, user + note, temperature, max_tokens, usage, label)
        problems = checker(text)
        if not problems:
            log(f"[{label}] passed gate")
            return text, attempt, []
        log(f"[{label}] gate problems:\n  - " + "\n  - ".join(problems))
        note = ("\n\n## DEFICIENCIES IN YOUR PREVIOUS OUTPUT — fix exactly these, "
                "keep everything else:\n- " + "\n- ".join(problems))
        if extra_note:
            note += "\n" + extra_note
    # targeted repair pass: rewrite only offending sentences
    if REPAIR_STAGES and label in REPAIR_STAGES and problems:
        log(f"[{label}] targeted repair pass")
        repair_user = ("Here is a text with specific problems.\n\nPROBLEMS (with quoted contexts):\n- "
                       + "\n- ".join(problems)
                       + "\n\nRewrite ONLY the sentences implicated above; keep every other sentence identical. "
                         "Output the complete corrected text, nothing else.\n\nTEXT:\n" + text)
        repaired, _ = call_llm(model, "You are a careful line editor.", repair_user,
                               0.3, max_tokens, usage, label + "-repair")
        rproblems = checker(repaired)
        if len(rproblems) < len(problems):
            log(f"[{label}] repair improved ({len(problems)} -> {len(rproblems)} problems)")
            text, problems = repaired, rproblems
    return text, MAX_TRIES, problems


def extract_json(text):
    """Tolerant JSON extraction from a model response."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.S)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        start = t.find("{")
        depth = 0
        for i in range(start, len(t)):
            if t[i] == "{":
                depth += 1
            elif t[i] == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(t[start:i + 1])
        raise


def reader_questions_section(plan):
    m = re.search(r"^#{1,4}\s+READER QUESTIONS\b(.*?)(?=^#{1,4}\s|\Z)", plan, re.M | re.S)
    return m.group(1).strip() if m else "(not found)"


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep-id", required=True)
    ap.add_argument("--foreground", required=True, help="foregrounded character id, e.g. char_sangwan")
    ap.add_argument("--places", required=True, help="comma-separated place ids (foregrounded locations)")
    ap.add_argument("--tags", required=True, help="comma-separated 8 tag ids")
    ap.add_argument("--model-plan", required=True)
    ap.add_argument("--model-prose", required=True)
    ap.add_argument("--model-format", required=True)
    ap.add_argument("--model-probe", default=None,
                    help="probe reader/judge model; defaults to --model-plan")
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()
    probe_model = args.model_probe or args.model_plan

    tag_ids = [t.strip() for t in args.tags.split(",") if t.strip()]
    assigned_anchors = assign_anchors(tag_ids)
    anchor_list = "\n".join(f"{tid} ({assign_anchors([tid])[tid][1] if assign_anchors([tid])[tid] else ''}): {assigned_anchors[tid][0]}" for tid in tag_ids)
    if len(tag_ids) != 8:
        raise SystemExit("exactly 8 tag ids required")
    place_ids = [p.strip() for p in args.places.split(",") if p.strip()]

    usage = Usage()

    # ----- load inputs
    shared = read_file(os.path.join(WORLD_DIR, "shared_context.md"))
    char_ids = {c["id"] for c in load_json(os.path.join(REPO_PUBLIC, "characters.json"))}
    place_id_set = {p["id"] for p in load_json(os.path.join(REPO_PUBLIC, "places.json"))}

    # characters: PC + foreground + any character whose files exist alongside the
    # foregrounded one's places (extras) — keep it simple: PC, foreground, and
    # every char_*.md/json present in world dir that the driver can name.
    char_texts = [load_character_text("char_pricha"), load_character_text(args.foreground)]
    # include extras whose ids appear in the foreground character's file
    fg_text = char_texts[1]
    for cid in sorted(char_ids):
        if cid in (fg_text) and cid not in ("char_pricha", args.foreground, "char_narrator"):
            char_texts.append(load_character_text(cid))
    place_texts = [load_place_text(pid) for pid in place_ids]
    place_texts.append(load_place_text("place_veranda"))

    slots = {
        "SHARED_CONTEXT": shared,
        "CHARACTER_FILES": "\n\n".join(char_texts),
        "PLACE_FILES": "\n\n".join(place_texts),
        "EP_ID": args.ep_id,
        "TAGS_WITH_NAMES": resolve_tags(tag_ids),
        "ANCHOR_LIST": anchor_list,
        "FOREGROUNDED": args.foreground,
    }

    restart_note = ""
    final_ep, final_plan, final_prose, final_probe = None, None, None, None
    total_attempts = {"plan": 0, "prose": 0, "format": 0}

    for restart in range(1, MAX_RESTARTS + 2):
        log(f"\n===== FULL PIPELINE PASS {restart} =====")
        # ----- STAGE 1: plan
        plan_slots = dict(slots)
        if restart_note:
            plan_slots["SHARED_CONTEXT"] = shared + "\n\n## DEFICIENCY FROM PREVIOUS READER-PROBE (must fix in the new plan):\n" + restart_note
        plan, tries, probs = run_stage(
            usage, "plan", args.model_plan, 0.7, 8000,
            os.path.join(PROMPTS_DIR, "plan.md"), plan_slots,
            lambda t: check_plan(t, args.foreground))
        total_attempts["plan"] += tries
        if probs:
            log("[plan] WARNING: still failing after max tries; continuing with best effort")

        # ----- STAGE 2: prose
        prose_slots = dict(slots)
        prose_slots["PLAN"] = plan
        anchor_note = ("The 8 Thai anchor phrases you MUST include verbatim, exactly these strings: "
                       + "; ".join(a[0] for a in assigned_anchors.values() if a))
        prose, tries, probs = run_stage(
            usage, "prose", args.model_prose, 0.8, 14000,
            os.path.join(PROMPTS_DIR, "prose.md"), prose_slots,
            lambda t: check_prose(t, plan, assigned_anchors), extra_note=anchor_note)
        total_attempts["prose"] += tries
        if probs:
            log("[prose] WARNING: still failing after max tries; continuing with best effort")
        # checkpoint intermediates immediately (crash safety)
        try:
            with open(args.out + ".plan.md", "w", encoding="utf-8") as fh: fh.write(plan)
            with open(args.out + ".prose.md", "w", encoding="utf-8") as fh: fh.write(prose)
        except Exception as ce:
            log(f"[checkpoint] could not save intermediates: {ce}")

        # ----- STAGE 3: format (with prose->format fallback)
        ep = None
        fmt_errors = []
        for fmt_round in range(2):  # round 2 regenerates prose once
            def fmt_checker(text, _errs=[]):
                _errs.clear()
                try:
                    candidate = extract_json(text)
                except Exception as e:
                    _errs.append(f"JSON does not parse: {e}")
                    return _errs
                _errs.extend(validate_episode(candidate, args.ep_id, char_ids,
                                              place_id_set, set(tag_ids)))
                return _errs

            fmt_slots = {"PROSE": prose, "PLAN": plan,
                         "VALID_IDS": "Valid character ids: " + ", ".join(sorted(char_ids)) + "\nValid place ids: " + ", ".join(sorted(place_id_set))}
            fmt_text, tries, probs = run_stage(
                usage, "format", args.model_format, 0.2, 16000,
                os.path.join(PROMPTS_DIR, "format.md"), fmt_slots,
                fmt_checker,
                extra_note="You are reformatting only: do NOT rewrite or alter any sentence content; fix structure, counts, ids, and fields.")
            total_attempts["format"] += tries
            try:
                candidate = extract_json(fmt_text)
                fmt_errors = validate_episode(candidate, args.ep_id, char_ids,
                                              place_id_set, set(tag_ids))
                if not fmt_errors:
                    ep = candidate
                    break
            except Exception as e:
                fmt_errors = [f"JSON does not parse: {e}"]
            if fmt_round == 0:
                log("[format] still failing; regenerating prose once with the format errors attached, then reformatting")
                prose_slots["PLAN"] = plan + ("\n\n## FORMAT-STAGE FAILURES ON THE LAST PROSE — write so the formatter can hit exact segment counts and schema:\n- "
                                              + "\n- ".join(fmt_errors))
                prose, tries2, _ = run_stage(
                    usage, "prose", args.model_prose, 0.8, 14000,
                    os.path.join(PROMPTS_DIR, "prose.md"), prose_slots,
                    lambda t: check_prose(t, plan))
                total_attempts["prose"] += tries2
        if ep is None:
            log("[format] FAILED after prose+format retry; restarting whole pipeline")
            restart_note = "The previous attempt failed mechanical JSON validation:\n- " + "\n- ".join(fmt_errors)
            continue

        # checkpoint the formatted episode before probing
        try:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(ep, fh, ensure_ascii=False, indent=1)
            log(f"[checkpoint] episode saved to {args.out} (pre-probe)")
        except Exception as ce:
            log(f"[checkpoint] could not save episode: {ce}")
        # ----- READER-COMPREHENSION PROBE
        log("[probe] zero-context reader call")
        probe_text, _ = call_llm(
            probe_model,
            "You are a careful reader answering questions about a text.",
            PROBE_QUESTIONS + "\n\n## EPISODE JSON\n" + strip_ids(ep),
            0.3, 4000, usage, "probe-reader")
        log("[probe] judge call")
        judge_text, _ = call_llm(
            probe_model,
            "You are a strict but fair judge.",
            JUDGE_PROMPT + "\n\n## (A) PLANNED READER ANSWERS\n" + reader_questions_section(plan)
            + "\n\n## (B) NAIVE READER'S ANSWERS\n" + probe_text,
            0.2, 2000, usage, "probe-judge")
        verdicts = re.findall(r"Q(\d):\s*(PASS|FAIL)\s*—?\s*(.*)", judge_text)
        for qn, v, reason in verdicts:
            log(f"[probe] Q{qn}: {v} — {reason.strip()}")
        fails = [(qn, reason.strip()) for qn, v, reason in verdicts if v == "FAIL"]
        final_ep, final_plan, final_prose = ep, plan, prose
        final_probe = (probe_text, judge_text, verdicts)
        if not fails:
            log("[probe] all reader questions PASS — episode accepted")
            break
        restart_note = ("The reader-comprehension probe FAILED these questions; the new episode must make these facts explicit on the page:\n"
                        + "\n".join(f"- Q{qn}: {reason}" for qn, _, reason in fails)
                        + "\n\nNaive reader's answers were:\n" + probe_text)
        log(f"[probe] {len(fails)} FAIL(s); restarting from stage 1 with deficiency note")
    else:
        pass

    # ----- outputs
    if final_ep is not None:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(final_ep, f, ensure_ascii=False, indent=2)
        log(f"[out] wrote {args.out}")
        base, _ = os.path.splitext(args.out)
        for suffix, text in ((".plan.md", final_plan), (".prose.md", final_prose)):
            if text:
                with open(base + suffix, "w", encoding="utf-8") as f:
                    f.write(text)
                log(f"[out] wrote {base}{suffix}")

    report = []
    report.append(f"# Pipeline report — {args.ep_id}")
    report.append(f"- models: plan={args.model_plan}, prose={args.model_prose}, format={args.model_format}")
    report.append(f"- attempts used: plan={total_attempts['plan']}, prose={total_attempts['prose']}, format={total_attempts['format']}")
    report.append(f"- tokens: prompt={usage.prompt}, completion={usage.completion}")
    report.append(f"- cost estimate: ${usage.cost:.4f} (MODEL_PRICES in driver.py; update per model)")
    report.append(f"- final status: {'SUCCESS' if final_ep is not None and final_probe and all(v=='PASS' for _,v,_ in final_probe[2]) else ('JSON OK, probe issues' if final_ep is not None else 'FAILED')}")
    report.append("\n## Log\n```")
    report.extend(log_lines)
    report.append("```")
    if final_probe:
        report.append("\n## Probe — naive reader answers\n```\n" + final_probe[0] + "\n```")
        report.append("\n## Probe — judge verdicts\n```\n" + final_probe[1] + "\n```")
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    log(f"[out] wrote {args.report}")

    if final_ep is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
