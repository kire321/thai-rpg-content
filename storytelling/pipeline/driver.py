#!/usr/bin/env python3
"""
3-stage episode-writing pipeline driver (plan -> prose -> JSON format)
with mechanical validation gates.

Design rules (sprint 1):
- Each stage runs EXACTLY ONCE. If a gate fails, the errors are recorded in
  the report and the pipeline continues with the best-effort output (or exits
  cleanly if the JSON cannot be parsed). No regeneration, no restarts.
- Character-agnostic: per-episode secrets come from the foregrounded
  character's private plan (storytelling/private/char_*_private.md), which is
  shown ONLY to the planner. The writer and formatter never see it; the
  planner's outline must contain only concrete events, never secret facts.
- Nicknames only: full-name introductions ("Pricha — Lek to the whole
  landing") are gone. Names come from public/characters.json and are enforced
  mechanically (full-name scan in the gates).
- Tag/vocab procedure: the planner picks ONE English anchor word per tag; the
  writer places that word in the line immediately preceding the tag marker;
  the formatter turns markers into tag segments. No Thai-phrase-with-gloss.

Stdlib + urllib only.

Usage:
  python3 driver.py --ep-id ep_002 --foreground char_sangwan \
      --places place_letter_writers_landing,place_pawnshop \
      --tags tag_254,tag_083,tag_167,tag_154,tag_337,tag_120,tag_197,tag_041 \
      --model-plan MODEL --model-prose MODEL --model-format MODEL \
      --out /path/out.json --report /path/report.md
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

WORLD_DIR = "/mnt/agents/output/world"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_PUBLIC = os.path.join(REPO_ROOT, "public")
PRIVATE_DIR = os.path.join(REPO_ROOT, "storytelling", "private")
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(PIPELINE_DIR, "prompts")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# $ per 1M tokens: {"model": (prompt, completion)} — extend/override as needed.
MODEL_PRICES = {
    "deepseek/deepseek-v3.2": (0.269, 0.40),
    "deepseek/deepseek-v4-flash": (0.0886, 0.1772),
    "qwen/qwen3-235b-a22b-2507": (0.09, 0.55),
    "default": (1.0, 5.0),
}

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
    payload = {
        "model": model,
        "stream": True,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    # sprint-5 lever 2: cap the reasoning burn on reasoning models
    # (v4-flash's unbounded reasoning truncates prose calls)
    if "v4-flash" in model:
        payload["reasoning"] = {"effort": "low"}
        payload["reasoning_effort"] = "low"
    payload_json = json.dumps(payload)
    req = urllib.request.Request(
        API_URL,
        data=payload_json.encode("utf-8"),
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
            with urllib.request.urlopen(req, timeout=180) as resp:
                raw = resp.read().decode("utf-8", "replace")
            # parse SSE stream into a normal completion-shaped dict
            chunks = []
            u = {}
            fr = None
            for line in raw.splitlines():
                line = line.strip()
                if not line.startswith("data:"):
                    continue
                payload_line = line[5:].strip()
                if payload_line == "[DONE]":
                    break
                try:
                    c = json.loads(payload_line)
                except json.JSONDecodeError:
                    continue
                if "usage" in c and c["usage"]:
                    u = c["usage"]
                ch = (c.get("choices") or [{}])[0]
                delta = ch.get("delta") or {}
                if delta.get("content"):
                    chunks.append(delta["content"])
                if ch.get("finish_reason"):
                    fr = ch["finish_reason"]
            data = {"choices": [{"message": {"content": "".join(chunks)}, "finish_reason": fr}], "usage": u}
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
    rt = ((data.get("usage") or {}).get("completion_tokens_details") or {}).get("reasoning_tokens")
    log(f"[api] {label}: model={model} tokens in={p} out={c}"
        + (f" reasoning={rt}" if rt is not None else ""))
    return msg, data["choices"][0].get("finish_reason")


# ---------------------------------------------------------------- file input
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_world_file(prefix_id):
    """char_x / place_x -> prefer <id>.md, then <id>.json (public versions only)."""
    for cand in (f"{prefix_id}.md", f"{prefix_id}.json"):
        p = os.path.join(WORLD_DIR, cand)
        if os.path.exists(p):
            return read_file(p)
    return None


def load_character_text(char_id):
    """Public character text — safe to show every stage (no secrets)."""
    text = find_world_file(char_id)
    if text is not None:
        return f"### {char_id}\n{text}"
    chars = load_json(os.path.join(REPO_PUBLIC, "characters.json"))
    for c in chars:
        if c.get("id") == char_id:
            return f"### {char_id} ({c.get('name','')})\n{c.get('description','')}"
    log(f"[warn] no data found for character {char_id}")
    return f"### {char_id}\n(no file found)"


def load_private_text(char_id):
    """The character's private plan (secrets). PLANNER ONLY — never downstream."""
    p = os.path.join(PRIVATE_DIR, f"{char_id}_private.md")
    if os.path.exists(p):
        return read_file(p)
    log(f"[warn] no private plan found for {char_id} in {PRIVATE_DIR}")
    return None


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


# ---------------------------------------------------------------- names
def build_name_map():
    """char_id -> (full_name, nickname_or_None), parsed from characters.json.

    Handles 'Pricha (Lek)', 'Sangwan (Wan)', and "Pornchai 'Pom' Boonyakam".
    """
    out = {}
    for c in load_json(os.path.join(REPO_PUBLIC, "characters.json")):
        cid = c.get("id", "")
        name = (c.get("name") or "").strip()
        if cid == "char_narrator" or not name:
            continue
        m = re.search(r"^(.+?)\s*\(([^)]+)\)", name)          # Full (Nick)
        if m:
            out[cid] = (m.group(1).strip(), m.group(2).strip())
            continue
        m = re.search(r"^(\w+)\s*'([^']+)'", name)            # Full 'Nick' Surname
        if m:
            out[cid] = (m.group(1).strip(), m.group(2).strip())
            continue
        out[cid] = (name, None)
    return out


def nickname_guide(name_map):
    lines = []
    for cid, (full, nick) in sorted(name_map.items()):
        if nick:
            lines.append(f"- {cid}: call them \"{nick}\" — NEVER \"{full}\".")
        else:
            lines.append(f"- {cid}: call them \"{full}\".")
    return "\n".join(lines)


def full_name_problems(text, name_map, where):
    """Flag any use of a full name when a nickname exists (word-boundary)."""
    problems = []
    for cid, (full, nick) in name_map.items():
        if not nick or full.lower() == nick.lower():
            continue
        m = re.search(r"\b" + re.escape(full) + r"\b", text, re.I)
        if m:
            problems.append(
                f"{where}: full name {full!r} used for {cid} — use the nickname {nick!r} "
                f"(...{text[max(0,m.start()-30):m.end()+30]!r}...)")
    return problems


# ---------------------------------------------------------------- tags
def resolve_tags(tag_ids):
    """English-only tag summaries for the shortlist: theme derived from the
    linked vocab items' English fields. NO Thai anywhere (the frontend's
    vocab quiz must not be given away by the story)."""
    tags = load_json(os.path.join(REPO_PUBLIC, "tags.json"))
    vocab = load_json(os.path.join(REPO_PUBLIC, "vocab_items.json"))
    by_id = {t["id"]: t for t in tags}
    out = []
    for tid in tag_ids:
        t = by_id.get(tid)
        if t is None:
            raise SystemExit(f"unknown tag id: {tid}")
        items = [v for v in vocab if v["id"] in set(t["vocab_item_ids"])]
        glosses = ", ".join(v["english"] for v in items[:12])
        out.append(f"{tid} — theme: {t['name']}\n  English glosses of linked vocab items: {glosses}")
    return "\n".join(out)


def extract_english_anchors(plan, tag_ids=None):
    """Parse the planner's TAG PLAN for one English anchor word per tag.

    Expected bullet shape: `- tag_254 — English anchor word: "word" — act N ...`
    Returns {tag_id: word}. tag_ids=None -> all tags found in the TAG PLAN.
    """
    m = re.search(r"^#{1,4}\s+TAG PLAN\b(.*?)(?=^#{1,4}\s|\Z)", plan, re.M | re.S)
    text = m.group(1) if m else plan
    anchors = {}
    for tid, word in re.findall(
            r"(tag_\d+)[^\n]*?English anchor word:\s*[\"“']?([A-Za-z][A-Za-z'-]*)", text, re.I):
        if tag_ids is None or tid in tag_ids:
            anchors[tid] = word.lower()
    return anchors


def extract_picked_tags(plan):
    """The planner's chosen 8 tags and their act assignments, from TAG PLAN
    bullets: `- tag_xxx — ... — act N, position ...`. Returns
    (ordered_tag_ids, {tag_id: act_num})."""
    m = re.search(r"^#{1,4}\s+TAG PLAN\b(.*?)(?=^#{1,4}\s|\Z)", plan, re.M | re.S)
    text = m.group(1) if m else ""
    picked, acts = [], {}
    for tid, act in re.findall(r"-\s*(tag_\d+)\b[^\n]*?—\s*act\s*([1-4])\b", text, re.I):
        if tid not in acts:
            picked.append(tid)
            acts[tid] = int(act)
    return picked, acts


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
# Technique vocabulary that must never reach the writer (the writer bug was
# naming techniques instead of executing them). The outline carries only
# concrete events, objects, dialogue content, and sensory details.
TECHNIQUE_VOCAB = [
    "wonder beat", "wonder", "refrain", "thesis", "show don't tell", "show, don't tell",
    "show don’t tell", "numinous", "elegiac", "connoisseur", "loving inventory",
    "dialectic", "dialectical", "foreshadow", "symbol", "symbolic", "motif",
    "theme", "thematic", "character arc", "tension", "poignant",
    "bittersweet", "lyrical", "evocative",
]

PLAN_SECTIONS = ["STICKY SITUATION", "OUTLINE", "TAG PLAN"]

STOPWORDS = {
    "the", "and", "that", "this", "with", "from", "into", "your", "yours",
    "have", "has", "had", "been", "will", "would", "could", "should", "must",
    "shall", "they", "them", "their", "there", "here", "what", "when",
    "which", "while", "until", "before", "after", "about", "over", "under",
    "then", "than", "once", "again", "still", "only", "just", "even", "some",
    "any", "very", "much", "more", "most", "upon", "down", "away", "back",
    "now", "how", "why", "who", "whom", "whose", "does", "did", "done",
    "make", "made", "making", "tell", "told", "says", "said", "goes",
    "going", "gone", "come", "came", "take", "took", "give", "gave", "keep",
    "kept", "puts", "sees", "without", "checking", "aloud", "version of",
}

SPEECH_VERBS = re.compile(
    r"\b(says|say|asks|asked|replies|replied|answers|answered|whispers|whispered|"
    r"calls|called|murmurs|murmured|shouts|shouted|demands|demanded|states|stated|"
    r"tells|told|speaks|spoke|cries|cried|announces|announced)\b|[“\"]", re.I)


def _act_sections(plan):
    """Yield (act_number, body_text) for each '### Act N' subsection of OUTLINE."""
    m = re.search(r"^##\s+OUTLINE\b(.*?)(?=^#{1,2}\s|\Z)", plan, re.M | re.S)
    text = m.group(1) if m else plan
    parts = re.split(r"^#{3,4}\s+Act\s+([1-4])\b[^\n]*$", text, flags=re.M)
    # parts: [pre, "1", body1, "2", body2, ...]
    for i in range(1, len(parts) - 1, 2):
        yield int(parts[i]), parts[i + 1]


def _beats(body):
    """Numbered beats of an act body: list of (beat_no, text)."""
    return [(int(n), t.strip()) for n, t in
            re.findall(r"^\s*(\d+)\.\s+(.+?)(?=^\s*\d+\.\s|\Z)", body, re.M | re.S)]


def _names_in(text, name_map):
    """Character ids whose full name or nickname appears in the text."""
    found = set()
    for cid, (full, nick) in name_map.items():
        variants = {full, nick} - {None}
        if full and full.lower().startswith("the "):
            variants.add(full[4:])
        for nm in variants:
            if nm and re.search(r"\b" + re.escape(nm) + r"\b", text, re.I):
                found.add(cid)
                break
    return found


def _content_words(text):
    words = re.findall(r"[A-Za-z]{4,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


MACHINERY_LABEL_RE = re.compile(
    r"^\s*(?:\d+\.\s*)?(?:WONDER|REFRAIN|THESIS|STAKES|SUBPLOT|ENTRANCE|DECISION|TAG)\b[^\n]*$", re.M | re.I)
LABEL_BEAT_RE = re.compile(r"^\s*(?:\d+\.\s*)?(WONDER|REFRAIN|THESIS)\b[^\n]*$", re.M | re.I)
COSMIC_RE = re.compile(r"\b(sky|skies|sea|stars?|moon|sun|world|turning|horizon|cosmos|tide)\b", re.I)


def check_plan(plan, shortlist, name_map, allowed_place_names, all_place_names):
    problems = []
    # models sometimes echo the nickname guide into the outline; strip those
    # lines before scanning so the guide itself doesn't trip the name gate
    plan = "\n".join(ln for ln in plan.splitlines()
                     if not ('call them "' in ln and "NEVER" in ln))
    for name in PLAN_SECTIONS:
        if not re.search(rf"^#{{1,4}}\s+{re.escape(name)}\b", plan, re.M):
            problems.append(f"missing mandatory section header: '{name}'")
    acts = dict(_act_sections(plan))
    if sorted(acts) != [1, 2, 3, 4]:
        problems.append(f"OUTLINE must have '### Act 1' ... '### Act 4' subsections (found acts: {sorted(acts) or 'none'})")
    # technique scan: machinery beat-labels are allowed (they are planner
    # instructions, never shown to the writer as vocabulary)
    scrubbed = MACHINERY_LABEL_RE.sub("", plan)
    low = scrubbed.lower()
    for tv in TECHNIQUE_VOCAB:
        if tv in low:
            i = low.find(tv)
            problems.append(f"technique vocabulary {tv!r} in the outline: ...{scrubbed[max(0,i-40):i+40]!r}... "
                            "(the outline lists concrete events only — the writer must never see technique words)")
    # beats are direct assertions: no comparisons anywhere in the outline
    similes = len(re.findall(r"\bas if\b|\blike\b", plan, re.I))
    if similes > 0:
        problems.append(f"outline contains {similes} comparison(s) ('like'/'as if'); beats must be direct "
                        "assertions (the writer expands whatever the outline contains — give it no comparisons)")
    # zero Thai anywhere (Change set A: the link is entirely in English)
    thai_found = re.findall(r"[฀-๿]+", plan)
    if thai_found:
        problems.append(f"outline contains Thai text ({thai_found[0][:20]}...) — NO Thai anywhere; "
                        "the frontend's vocab quiz must not be given away")
    # TAG PLAN: exactly 8 tags from the shortlist, 2 per act, distinct
    # English anchor words
    picked, picked_acts = extract_picked_tags(plan)
    if len(picked) != 8:
        problems.append(f"TAG PLAN must pick exactly 8 tags from the shortlist (found {len(picked)})")
    outside = [t for t in picked if t not in shortlist]
    if outside:
        problems.append(f"TAG PLAN picks tags not on the shortlist: {outside}")
    act_counts = {}
    for t, a in picked_acts.items():
        act_counts[a] = act_counts.get(a, 0) + 1
    if picked and act_counts != {1: 2, 2: 2, 3: 2, 4: 2}:
        problems.append(f"TAG PLAN must assign exactly 2 tags per act (got {act_counts})")
    anchors = extract_english_anchors(plan)
    missing = [t for t in picked if t not in anchors]
    if missing:
        problems.append(f"TAG PLAN is missing a parseable English anchor word for: {missing} "
                        "(expected bullet shape: '- tag_xxx — English anchor word: \"word\" — act N ...')")
    if len(set(anchors.values())) != len(anchors):
        problems.append(f"English anchor words must all be different (got {sorted(anchors.values())})")
    all_beats = [(a, n, t) for a in sorted(acts) for n, t in _beats(acts[a])]
    # --- literary machinery gates (labels only; content is the planner's art)
    # label beats may be numbered or not — scan the raw act bodies
    label_lines = [(a, ln.strip()) for a in sorted(acts)
                   for ln in acts[a].splitlines() if LABEL_BEAT_RE.match(ln)]
    thesis = [(a, ln) for a, ln in label_lines if re.match(r"\s*(?:\d+\.\s*)?THESIS\b", ln, re.I)]
    if len(thesis) < 3 or not any(a == 1 for a, ln in thesis):
        problems.append("thesis noun phrase: need a THESIS beat in act 1 (the opening line) "
                        "plus at least 2 later THESIS occurrences")
    else:
        # dialectical variety: at least 2 DISTINCT phrases from the private
        # plans; no phrase repeated across more than 2 beats
        phrases = []
        for a, ln in thesis:
            pm = re.search(r"THESIS\s*[\"“](.+?)[\"”]", ln, re.I)
            phrases.append(pm.group(1).strip().lower() if pm else ln.lower())
        if len(set(phrases)) < 2:
            problems.append("dialectical phrase variety: the THESIS beats all carry ONE phrase — "
                            "use at least 2 DISTINCT phrases drawn from the character's AND the "
                            "place's private plans when available")
        for ph in set(phrases):
            if phrases.count(ph) > 2:
                problems.append(f"dialectical phrase variety: phrase {ph[:40]!r} appears on "
                                f"{phrases.count(ph)} beats (max 2) — vary which phrase a "
                                "beat carries")
        tm = re.search(r"THESIS\s*[\"“](.+?)[\"”]", thesis[0][1], re.I)
        # direct apposition: ban comparisons only ('like'/'as if'); 'of' is
        # allowed when the descriptor's properties apply literally to the
        # object ("clerk of other people's news" — he literally clerks them)
        if tm and re.search(r"\b(like|as)\b", tm.group(1), re.I):
            problems.append(f"thesis noun phrase {tm.group(1)!r} uses 'like'/'as' — it must be "
                            "direct apposition (\"the letter-writer, clerk of other people's news\")")
    refrain = [(a, ln) for a, ln in label_lines if re.match(r"\s*(?:\d+\.\s*)?REFRAIN\b", ln, re.I)]
    if len(refrain) != 3 or len({a for a, ln in refrain}) < 2:
        problems.append(f"refrain arc: need exactly 3 REFRAIN beats spread across at least 2 acts "
                        f"(found {len(refrain)})")
    else:
        wordings = [re.search(r"REFRAIN\s*[\"“](.+?)[\"”]", ln, re.I) for a, ln in refrain]
        wordings = [w.group(1).strip().lower() for w in wordings if w]
        if len(wordings) == 3 and len(set(wordings)) < 3:
            problems.append("refrain arc: the three occurrences must never be verbatim twice — "
                            "each rewords the refrain's core words")
        if refrain and not COSMIC_RE.search(refrain[-1][1]):
            problems.append("refrain arc: the final occurrence must be cosmic in scale "
                            "(sky/sea/stars/the turning world) while echoing the core words")
    wonder = [(a, ln) for a, ln in label_lines if re.match(r"\s*(?:\d+\.\s*)?WONDER\b", ln, re.I)]
    wacts = {a for a, ln in wonder}
    if wacts != {1, 2, 3, 4}:
        problems.append(f"wonder beats: need one WONDER beat per act (found acts {sorted(wacts)})")
    for a, ln in wonder:
        if not re.search(r"\b(inventory|numinous|connoisseur|elegiac)\b", ln, re.I):
            problems.append(f"act {a}: WONDER beat must name its shape "
                            "(inventory / numinous / connoisseur / elegiac) and supply the concrete content")
    problems.extend(full_name_problems(plan, name_map, "plan"))
    # places: scene locations (PRESENT lines) may only use allowed places;
    # dialogue/beats may freely MENTION other places
    present_lines = "\n".join(ln for ln in plan.splitlines() if ln.strip().upper().startswith("PRESENT:"))
    for pname in all_place_names - allowed_place_names:
        if len(pname) > 3 and pname.lower() in present_lines.lower():
            problems.append(f"a PRESENT line stages the scene at {pname!r}, which is not in this "
                            f"episode's allowed places ({sorted(allowed_place_names)})")
    if sorted(acts) != [1, 2, 3, 4]:
        return problems

    # ---- per-act structural checks
    present = {}   # act -> set of char ids in the PRESENT line
    introduced = set()  # chars with an ENTRANCE beat (or act-1 PRESENT) so far
    beats_text_so_far = ""  # non-decision beat text of acts processed so far
    for anum in (1, 2, 3, 4):
        body = acts[anum]
        beats = _beats(body)
        if not any(t.upper().startswith("DECISION") for n, t in beats):
            problems.append(f"act {anum}: no DECISION beat (every act needs exactly one, ending the act)")
        pm = re.search(r"^PRESENT:\s*(.+)$", body, re.M)
        if not pm:
            problems.append(f"act {anum}: missing 'PRESENT: ...' line naming who is on stage")
            present[anum] = set()
        else:
            present[anum] = _names_in(pm.group(1), name_map)
        if anum == 1:
            introduced |= present[1]
            # characters whose presence is obvious from the place (a clerk in
            # a salt store) need no introduction beat — the PRESENT line is
            # the general sense of who's in the scene. Only NON-obvious
            # characters need an ENTRANCE beat, and nobody may be revealed
            # present late who would obviously have been noticed.
            place_tokens = set()
            for pn in allowed_place_names:
                place_tokens |= {w for w in re.findall(r"[a-z]{3,}", pn.lower())
                                 if w not in ("the", "and")}
            for cid in present[1]:
                full, nick = name_map.get(cid, ("", ""))
                name_tokens = {w for w in re.findall(r"[a-z]{3,}", (full + " " + (nick or "")).lower())
                               if w not in ("the", "and")}
                obvious = bool(name_tokens & place_tokens) or cid == "char_pricha"
                if obvious:
                    continue
                intro = any(re.match(r"ENTRANCE\b", t, re.I) and cid in _names_in(t, name_map)
                            for n, t in beats if n <= 6)
                if not intro:
                    problems.append(f"act 1: {cid} is in the PRESENT line but gets no ENTRANCE beat in "
                                    "the first 6 beats — non-obvious characters must be introduced "
                                    "before they speak (place-obvious ones need no introduction)")
            # COMPOSED DENSITY: act-1 segment-1 beats (up to the first TAG
            # pair) must EACH carry 2+ plan elements; no 3+ consecutive
            # single-element beats anywhere in the outline.
            loaded_all = []
            for n, t in beats:
                cm = re.search(r"carries:\s*([^\n]+)$", t, re.I)
                loaded_all.append(len([e for e in cm.group(1).split(",") if e.strip()]) if cm else 1)
            tag_pos = [i for i, (n, t) in enumerate(beats)
                       if re.match(r"TAG\s+tag_\d+:", t, re.I)]
            seg1_end = (tag_pos[0] + 2) if tag_pos else 6
            for i, (n, t) in enumerate(beats[:seg1_end]):
                if i < len(loaded_all) and loaded_all[i] < 2 and not t.upper().startswith("DECISION"):
                    problems.append(f"act 1 beat {n}: opening-segment beat carries <2 plan elements — "
                                    "each opening beat must interlock (character intro AND "
                                    "stakes/setting/thesis in the same beat), not roster-sequencing")
            run = 0
            for c in loaded_all:
                run = run + 1 if c <= 1 else 0
                if run >= 3:
                    problems.append(f"act {anum}: a run of 3+ single-element beats — merge them so "
                                    "each beat carries multiple plan elements")
                    break
        # STAKES beat in act 1, early, naming a concrete cost
        if anum == 1:
            stakes = [n for n, t in beats if t.upper().startswith("STAKES:")]
            if not stakes:
                problems.append("act 1: no beat labeled 'STAKES:' (one early beat must be a character "
                                "stating aloud what they want and what it costs)")
            else:
                if stakes[0] > 6:
                    problems.append(f"act 1: STAKES beat is beat {stakes[0]} — it must land in the first 6 beats "
                                    "(segment 1)")
                stext = " ".join(t for n, t in beats if t.upper().startswith("STAKES:"))
                if not re.search(r"\b(or|otherwise|else|if not|unless)\b", stext, re.I):
                    problems.append("act 1: STAKES beat names no concrete cost — it must say what happens "
                                    "if the characters fail (\"X, or Y happens\")")
        # PC holds the thread: char_pricha must have an action/dialogue beat
        # in every act (not just inside decision outcomes)
        pc_beats = [n for n, t in beats
                    if not t.upper().startswith("DECISION") and "char_pricha" in _names_in(t, name_map)]
        if not pc_beats:
            problems.append(f"act {anum}: the PC (Lek) has no action or dialogue beat — he must hold "
                            "the central thread in every act, not only inside decision outcomes")
        # SUBPLOT plant: exactly one beat labeled SUBPLOT: somewhere in the outline
        if anum == 1:
            subplot = re.findall(r"^\s*\d+\.\s*SUBPLOT:", plan, re.M)
            if not subplot:
                problems.append("no beat labeled 'SUBPLOT:' — one beat must show the facet of the "
                                "foregrounded character's private plan this episode reveals or plants "
                                "(as a concrete event, never stating the secret)")
        # urgency: if any beat plants a deadline, act 3 must have a beat where
        # it converges
        if anum == 3:
            whole = " ".join(t for a in (1, 2, 3, 4) for n, t in _beats(acts.get(a, "")))
            dl = r"\b(noon|dawn|dusk|midnight|deadline|sunrise|sunset|tomorrow|days?\s+hence|by\s+(morning|evening)|mail[- ]boat)\b"
            planted = re.search(dl, " ".join(t for a in (1, 2) for n, t in _beats(acts.get(a, ""))), re.I)
            if planted and not re.search(dl, body, re.I):
                problems.append("act 3: a deadline is planted in acts 1-2 but no act-3 beat shows it "
                                "converging (act 3 is the maximally-urgent act)")
        # entrance-before-speech
        for n, t in beats:
            if t.upper().startswith(("STAKES:", "DECISION")):
                continue
            if re.match(r"TAG\s+tag_\d+:", t, re.I):
                # the TAG beat must create the dramatic pretext: who says the
                # Thai phrase, to whom, in what situation
                if not _names_in(t, name_map):
                    problems.append(f"act {anum} beat {n}: TAG beat names no character — the theme "
                                    "scene needs someone in it, doing or feeling the tag's theme")
                continue
            is_entrance = bool(re.match(r"ENTRANCE\b", t, re.I))
            if is_entrance:
                introduced |= _names_in(t, name_map)
                continue
            if SPEECH_VERBS.search(t):
                for cid in _names_in(t, name_map) - {"char_pricha"}:
                    if cid not in introduced:
                        problems.append(f"act {anum} beat {n}: {cid} speaks/acts in dialogue before any "
                                        "ENTRANCE beat or act-1 PRESENT line introduces them")
        # act-1 speaker budget: narrator + PC + at most one other speaker in
        # segment 1 (first 6 beats)
        if anum == 1:
            cut = 6
            speakers = set()
            for n, t in beats:
                if n > cut:
                    break
                if SPEECH_VERBS.search(t) and not t.upper().startswith("STAKES:"):
                    speakers |= _names_in(t, name_map)
            speakers.discard("char_pricha")
            if len(speakers) > 1:
                problems.append(f"act 1 opening stretch has {len(speakers)} non-PC speakers {sorted(speakers)}; "
                                "budget is narrator + PC + one other — move later speakers' beats after the "
                                "STAKES beat or into later acts")
        # beat budget: tag beat-pairs mark the segment boundaries; beats map
        # 1:1 to prose lines, so counts must land at seg1 4-6 / seg2 2-3 /
        # seg3 2-3 (DECISION beats excluded)
        content_beats = [(n, t) for n, t in beats if not t.upper().startswith("DECISION")]
        tag_idx = [i for i, (n, t) in enumerate(content_beats)
                   if re.match(r"TAG\s+tag_\d+:", t, re.I)]
        if len(tag_idx) == 2:
            # segment boundary is AFTER the reaction beat (TAG beat + 1)
            b1 = tag_idx[0] + 2
            b2 = tag_idx[1] + 2
            c1 = b1
            c2 = b2 - b1
            c3 = len(content_beats) - b2
            for cnt, lo, hi, sname in ((c1, 4, 6, "seg1"), (c2, 2, 3, "seg2"), (c3, 2, 3, "seg3")):
                if not (lo <= cnt <= hi):
                    problems.append(f"act {anum}: beat budget {sname} has {cnt} beats (need {lo}-{hi}) — "
                                    "place each TAG pair so segment line counts land")
        else:
            problems.append(f"act {anum}: expected exactly 2 TAG beat-pairs (found {len(tag_idx)}) — "
                            "each tag needs its 'TAG tag_xxx:' pretext beat followed by a reaction beat")
        # DECISION checks: choices built only from established facts; outcomes
        # bound to their choice's action/objects. Binding is measured by
        # content-word overlap with the established page (sticky situation +
        # beats so far) — verbs of the action itself need no prior establishment,
        # but the choice's objects/people/facts must already exist on the page.
        sticky = re.search(r"^##\s+STICKY SITUATION\b(.*?)(?=^#{1,2}\s|\Z)", plan, re.M | re.S)
        sticky_text = sticky.group(1) if sticky else ""
        for n, t in beats:
            if not t.upper().startswith("DECISION"):
                continue
            head = DECISION_HEAD_RE.search(t)
            if not head:
                problems.append(f"act {anum}: DECISION beat does not name the dilemma speaker — "
                                "expected 'DECISION — dilemma line (<nickname>): \"...\"'")
            else:
                dilemma = head.group(2).strip()
                # the dilemma must be a line the character would actually say,
                # not bare 'X or Y' imperative menu-text
                if "?" not in dilemma and len(dilemma.split()) < 12:
                    problems.append(f"act {anum}: dilemma line {dilemma[:60]!r} reads as bare 'X or Y' "
                                    "menu-text — write dialogue the character would actually say that "
                                    "poses the choice (a question, or a fuller spoken line)")
            n_opts = len(re.findall(r"\[(easy|medium|hard)\]", t))
            n_attrs = len(re.findall(r"\(attr_\w+\)", t))
            if n_opts != 3 or n_attrs != 3:
                problems.append(f"act {anum}: DECISION beat must have exactly 3 options "
                                f"[easy]/[medium]/[hard], each with an (attr_...) — found "
                                f"{n_opts} options, {n_attrs} attributes")
            for diff, opt, at, pout, fout in DECISION_OPTION_RE.findall(t):
                opt_facts = (sticky_text + " " + beats_text_so_far + " " + " ".join(
                    bt for bn, bt in beats if not bt.upper().startswith("DECISION"))).lower()
                opt_words = set(_content_words(opt))
                if len(opt_words & set(_content_words(opt_facts))) < min(2, len(opt_words)):
                    problems.append(f"act {anum} [{diff}] choice {opt[:60]!r} shares fewer than 2 content "
                                    "words with the page so far — choices may only use objects/facts/people "
                                    "the beats or sticky situation already established")
                for cid in _names_in(opt, name_map):
                    if cid not in (present.get(anum) or set()) and cid not in introduced:
                        problems.append(f"act {anum} [{diff}] choice references {cid}, who is not on stage "
                                        "and never entered")
                for label, oc in (("PASS", pout), ("FAIL", fout)):
                    if not oc.strip().startswith(("I ", "I'", "I’")):
                        problems.append(f"act {anum} [{diff}] {label} outcome does not begin with 'I ' — "
                                        "outcomes are the PC speaking in first person")
                    shared = set(_content_words(oc)) & (opt_words | set(_content_words(opt_facts)))
                    if not shared:
                        problems.append(f"act {anum} [{diff}] {label} outcome {oc[:50]!r} shares no content "
                                        "word with its choice or the scene's beats — outcomes must be a "
                                        "concrete event resulting from THAT choice's action, naming its "
                                        "objects")
        introduced |= present.get(anum, set())
        beats_text_so_far += " " + " ".join(
            t for n, t in beats if not t.upper().startswith("DECISION"))
    # dilemma-line syntax diversity: the 4 dilemma lines must not share one
    # template (4-of-4 identical first-3-words = failure)
    dilemma_openings = []
    for dm in DECISION_HEAD_RE.finditer(plan):
        words = re.findall(r"[a-z']+", dm.group(2).lower())
        if len(words) >= 3:
            dilemma_openings.append(" ".join(words[:3]))
    if len(dilemma_openings) == 4 and len(set(dilemma_openings)) == 1:
        problems.append(f"all 4 dilemma lines open identically ({dilemma_openings[0]!r}) — each "
                        "dilemma is in-character dialogue by a NAMED character reacting to THIS "
                        "situation, not PC-voiced menu text from one template")
    # double entrances: a character gets at most one ENTRANCE beat
    ent_seen = {}
    for m in re.finditer(r"^\s*(?:\d+\.\s*)?ENTRANCE\s+([^:]+):", plan, re.M | re.I):
        who = m.group(1).strip().lower()
        ent_seen[who] = ent_seen.get(who, 0) + 1
    for who, cnt in ent_seen.items():
        if cnt > 1:
            problems.append(f"{who} gets {cnt} ENTRANCE beats — a character enters once; later "
                            "mentions assume the entrance happened")
    # orphaned objects: an object that changes hands notably (pockets/tucks/
    # hides/stows/slips + the/a/his/her <noun>) must be referenced again in
    # a later beat
    flat = [(a, n, t) for a in sorted(acts) for n, t in _beats(acts[a])]
    for i, (a, n, t) in enumerate(flat):
        for vm in re.finditer(r"\b(?:pockets?|tucks?|hides|hid|stows?|slips?|stole|steals?)\s+"
                              r"(?:the|a|his|her|their|a single)\s+([a-z]+)", t, re.I):
            obj = vm.group(1)
            if len(obj) < 4:
                continue
            later = " ".join(t2 for a2, n2, t2 in flat[i + 1:])
            if not re.search(r"\b" + re.escape(obj) + r"s?\b", later, re.I):
                problems.append(f"act {a} beat {n}: the {obj} changes hands and is never referenced "
                                "again — an object moved must be accounted for by episode end")
    return problems


# markers may be on their own line OR trailing the sentence they follow
TAG_MARKER_RE = re.compile(r"\[\[\s*(tag_\d+)\s*\]\]")


ALLOWED_PLACES_TEXT = ""  # set by main() / caller so the prose gate can validate PLACE lines


def check_prose_act(act_text, anum, plan, act_tag_ids, name_map):
    """Per-act prose gate: the no-merge contract, tag placement, and all
    cheap lints, scoped to one act's text."""
    problems = []
    where = f"act {anum}"
    if re.findall(r"[฀-๿]+", act_text):
        problems.append(f"{where}: Thai text present — zero Thai allowed")
    if "*" in act_text:
        problems.append(f"{where}: markdown asterisk in prose")
    if not re.search(r"^PLACE:\s*\S", act_text, re.M):
        problems.append(f"{where}: no 'PLACE:' line")
    else:
        pm0 = re.search(r"^PLACE:\s*(.+?)\s*$", act_text, re.M)
        known_places = {p.strip().lower() for p in
                        re.findall(r"^-\s+(.+)$", ALLOWED_PLACES_TEXT, re.M)}
        if known_places and pm0.group(1).strip().lower() not in known_places:
            problems.append(f"{where}: PLACE {pm0.group(1).strip()!r} is not one of the allowed "
                            f"places {sorted(known_places)}")
    known = {"narrator"}
    for cid, (full, nick) in name_map.items():
        for nm in {full, nick} - {None}:
            known.add(nm.lower())
            if nm.lower().startswith("the "):
                known.add(nm[4:].lower())
    for ln in act_text.splitlines():
        s = ln.strip()
        if not s or s.startswith("#") or s.upper().startswith("PLACE:"):
            continue
        sm = re.match(r"^([^:#]{1,40}?):\s+", s)
        if not sm:
            problems.append(f"{where}: line has no 'Speaker:' prefix: {s[:60]!r}")
            continue
        if sm.group(1).strip().lower() not in known:
            problems.append(f"{where}: speaker prefix {sm.group(1).strip()!r} maps to no character "
                            "— use a nickname from the Names list or NARRATOR")
        if s.upper().startswith("NARRATOR:"):
            body = s[len("NARRATOR:"):]
            if '"' in body or "“" in body or "”" in body:
                problems.append(f"{where}: NARRATOR line contains quoted speech: {s[:60]!r}")
            elif re.search(r"\b(asks|says|said|replies|replied|answers|whispers|shouts|murmurs)\b",
                           body, re.I):
                problems.append(f"{where}: NARRATOR narrates speech ('X asks/says'): {s[:60]!r}")
            if re.search(r"\b(forged|forgery|fake|stolen)\b", body, re.I):
                problems.append(f"{where}: NARRATOR uses spoiler word (forged/fake/stolen): "
                                f"{s[:60]!r}")
        for jm in re.finditer(r"\[([^\]]+)\]", s):
            sd = jm.group(1).strip().lower()
            if re.fullmatch(r"(asks?|asked|responds?|responded|repl(y|ies|ied)|frowns?|sighs?|nods?|"
                            r"smiles?|says|said|murmurs?|whispers?|pauses?|continues?|adds?)", sd):
                problems.append(f"{where}: junk stage direction [{sd}] — physical content or empty")
    markers = TAG_MARKER_RE.findall(act_text)
    if sorted(markers) != sorted(act_tag_ids):
        problems.append(f"{where}: tag markers {sorted(markers)} != this act's assigned "
                        f"{sorted(act_tag_ids)} (exactly these 2, no others)")
    anchors = extract_english_anchors(plan)
    content = [ln for ln in act_text.splitlines()
               if ln.strip() and not ln.strip().startswith("#")
               and not ln.strip().upper().startswith("PLACE:")]
    if not (8 <= len(content) <= 12):
        problems.append(f"{where}: {len(content)} prose lines (contract 8-12)")
    groups, cur = [[]], []
    for ln in content:
        cur.append(ln)
        if TAG_MARKER_RE.search(ln):
            groups[-1] = cur
            cur = []
            groups.append(cur)
    groups[-1] = cur
    if len(groups) == 3:
        for gi, (lo, hi, sname) in enumerate(((4, 6, "segment 1"), (2, 3, "segment 3"),
                                              (2, 3, "segment 5"))):
            n = len(groups[gi])
            if not (lo <= n <= hi):
                problems.append(f"{where} {sname}: has {n} prose lines (expected {lo}-{hi}) — "
                                "rebalance lines around the markers")
    elif len(markers) == 2:
        problems.append(f"{where}: could not split into 3 segments around 2 markers")
    marks = [(m.start(), m.group(1)) for m in TAG_MARKER_RE.finditer(act_text)]
    for pos, tid in marks:
        word = anchors.get(tid)
        prev = ""
        for ln in reversed(act_text[:pos].splitlines()):
            if ln.strip():
                prev = ln
                break
        if word and not re.search(r"\b" + re.escape(word) + r"\b", prev, re.I):
            problems.append(f"{where}: marker [[{tid}]]'s preceding line lacks the English anchor "
                            f"word {word!r} (prev: {prev.strip()[:60]!r})")
    similes = len(re.findall(r"\bas if\b|\blike\b", act_text, re.I))
    if similes > 0:
        problems.append(f"{where}: {similes} comparison(s) ('like'/'as if') — direct assertions only")
    for fp in full_name_problems(act_text, name_map, where):
        problems.append(f"{where}: {fp}")
    low = act_text.lower()
    for tv in TECHNIQUE_VOCAB:
        if tv in low:
            problems.append(f"{where}: technique vocabulary {tv!r} in the prose — delete or rephrase")
    return problems


def check_prose(prose, plan, tag_ids, name_map):
    problems = []
    # zero Thai anywhere (hard rule: the story must never give away the quiz)
    thai_found = re.findall(r"[฀-๿]+", prose)
    if thai_found:
        problems.append(f"prose contains Thai text ({thai_found[0][:20]}...) — NO Thai anywhere; "
                        "the story/tag link is entirely in English")
    if len(re.findall(r"^#{1,3}\s+Act\s+\d", prose, re.M)) != 4:
        problems.append("prose does not contain exactly four '## Act N' sections")
    # every speaker prefix must map to a known character (or NARRATOR) —
    # the deterministic formatter hard-fails on anything it cannot map
    known = {"narrator"}
    for cid, (full, nick) in name_map.items():
        for nm in {full, nick} - {None}:
            known.add(nm.lower())
            if nm.lower().startswith("the "):
                known.add(nm[4:].lower())
    bad_speakers = {}
    for ln in prose.splitlines():
        stripped = ln.strip()
        if stripped.upper().startswith("PLACE:"):
            continue
        sm = re.match(r"^([^:#]{1,40}?):\s+", stripped)
        if sm and sm.group(1).strip().lower() not in known:
            bad_speakers.setdefault(sm.group(1).strip(), stripped[:60])
    for spk, ctx in bad_speakers.items():
        problems.append(f"speaker prefix {spk!r} maps to no character ({ctx!r}) — rename it to a "
                        "nickname from the Names list, or make the line NARRATOR:")
    # cheap lints
    if "*" in prose:
        i = prose.index("*")
        problems.append(f"markdown asterisk in prose: ...{prose[max(0,i-40):i+40]!r}... — no markdown "
                        "formatting in story text")
    # junk stage directions: [asks]/[responds]/[frowns]/[sighs] merely restate
    # the speech act — physical content or nothing
    for jm in re.finditer(r"\[([^\]]+)\]", prose):
        sd = jm.group(1).strip().lower()
        if re.fullmatch(r"(asks?|asked|responds?|responded|repl(y|ies|ied)|frowns?|sighs?|nods?|smiles?|"
                        r"says|said|murmurs?|whispers?|pauses?|continues?|adds?)", sd):
            problems.append(f"junk stage direction [{sd}] — it merely restates the speech act; give it "
                            "physical content or drop the brackets")
    # actions live in [stage directions]; dialogue belongs to the speaker.
    # A NARRATOR line must never carry quoted speech or 'X asks/says/replies',
    # and must never spoil an unrevealed fact (forged/fake/stolen)
    for ln in prose.splitlines():
        s = ln.strip()
        if not s.upper().startswith("NARRATOR:"):
            continue
        body0 = s[len("NARRATOR:"):]
        if re.search(r"\b(forged|forgery|fake|stolen)\b", body0, re.I):
            problems.append(f"NARRATOR line uses a spoiler word (forged/fake/stolen): {s[:70]!r} — the "
                            "narrator may not deliver a verdict the episode hasn't revealed yet")
        body = s[len("NARRATOR:"):]
        if '"' in body or "“" in body or "”" in body:
            problems.append(f"NARRATOR line contains quoted speech: {s[:70]!r} — give the speech to "
                            "the speaking character as '<Nickname>: [action] \"words\"'")
        elif re.search(r"\b(asks|says|said|replies|replied|answers|whispers|shouts|murmurs)\b", body, re.I):
            problems.append(f"NARRATOR line narrates speech ('X asks/says'): {s[:70]!r} — the words "
                            "belong to the speaking character's own line")
    markers = TAG_MARKER_RE.findall(prose)
    if sorted(markers) != sorted(tag_ids):
        picked_acts = extract_picked_tags(plan)[1]
        missing = [t for t in tag_ids if t not in markers]
        placement = "; ".join(f"{t} belongs in act {picked_acts.get(t, '?')}" for t in missing)
        problems.append(f"tag markers {sorted(markers)} != assigned set {sorted(tag_ids)} "
                        f"(each tag needs exactly one marker '[[tag_xxx]]' at the end of the line "
                        f"carrying its English anchor word). MISSING: {placement or 'none'}")
    # no comparison flood — the outline had none, so the prose may add none
    similes = len(re.findall(r"\bas if\b|\blike\b", prose, re.I))
    if similes > 2:
        problems.append(f"prose contains {similes} comparisons ('like'/'as if'); max 2 — state images "
                        "directly instead of comparing them")
    # each marker: the tag's English anchor word in the line immediately
    # before it. Markers may be on their own line or trailing the sentence.
    anchors = extract_english_anchors(plan)
    marks = [(m.start(), m.group(1)) for m in TAG_MARKER_RE.finditer(prose)]
    act_heads = [m.start() for m in re.finditer(r"^#{1,3}\s+Act\s+\d", prose, re.M)]
    # segment line counts per act: 4-6 lines before marker 1, 2-3 between
    # markers, 2-3 after marker 2 (structured prose lines only)
    act_chunks = re.split(r"^#{1,3}\s+Act\s+\d[^\n]*$", prose, flags=re.M)[1:]
    for ai, chunk in enumerate(act_chunks, 1):
        pm = re.search(r"^PLACE:\s*(.+?)\s*$", chunk, re.M)
        if not pm:
            problems.append(f"act {ai}: no 'PLACE:' line (the formatter needs one per act, "
                            "copied exactly from the allowed place names)")
        else:
            known_places = {p.strip().lower() for p in
                            re.findall(r"^-\s+(.+)$", ALLOWED_PLACES_TEXT, re.M)}
            if known_places and pm.group(1).strip().lower() not in known_places:
                problems.append(f"act {ai}: PLACE {pm.group(1).strip()!r} is not one of the allowed "
                                f"places {sorted(known_places)} — restage the act at an allowed place")
        content = [ln for ln in chunk.splitlines()
                   if ln.strip() and not ln.strip().upper().startswith("PLACE:")]
        groups, cur = [[]], []
        for ln in content:
            has_marker = bool(TAG_MARKER_RE.search(ln))
            cur.append(ln)
            if has_marker:
                groups[-1] = cur
                cur = []
                groups.append(cur)
        groups[-1] = cur
        if len(groups) == 3:
            for gi, (lo, hi, sname) in enumerate(((4, 6, "segment 1"), (2, 3, "segment 3"),
                                                  (2, 3, "segment 5"))):
                n = len(groups[gi])
                if not (lo <= n <= hi):
                    problems.append(f"act {ai} {sname}: has {n} prose lines (expected {lo}-{hi}) — "
                                    "rebalance lines around the markers")
    for k, (pos, tid) in enumerate(marks):
        word = anchors.get(tid)
        start = max([0] + [p for p, _ in marks[:k]] + [h for h in act_heads if h < pos])
        before = prose[start:pos]
        prev = ""
        for ln in reversed(before.splitlines()):
            if ln.strip():
                prev = ln
                break
        if word and not re.search(r"\b" + re.escape(word) + r"\b", prev, re.I):
            problems.append(f"marker [[{tid}]]: the line immediately before it does not use the "
                            f"English anchor word {word!r} (prev line: {prev.strip()[:70]!r})")
    low = prose.lower()
    for tv in TECHNIQUE_VOCAB:
        if tv in low:
            i = low.find(tv)
            problems.append(f"technique vocabulary {tv!r} appears in the prose: ...{prose[max(0,i-40):i+40]!r}...")
    problems.extend(full_name_problems(prose, name_map, "prose"))
    return problems


# ---------------------------------------------------------------- JSON validation
SEG_PATTERN = ["narrative", "tag", "narrative", "tag", "narrative"]
ATTRIBUTES = {"attr_heart_water", "attr_deference", "attr_ledger",
              "attr_word_hoard", "attr_merit_water"}


def wc(s):
    return len(s.split())


def validate_line(line, char_ids, place_ids, name_map, where, errors, allowed_places=None):
    if not isinstance(line, dict):
        errors.append(f"{where}: line is not an object")
        return
    # Narrator acid test: a non-narrator line must never mention its own
    # speaker in third person — that is narration misattributed.
    spk = line.get("character", "")
    dlg = line.get("dialogue", "") or ""
    if spk and spk != "char_narrator" and spk.startswith("char_") and dlg:
        full, nick = name_map.get(spk, (spk[len("char_"):], None))
        tokens = {t for t in (full, nick) if t}
        for tok in tokens:
            if re.search(r"\b" + re.escape(tok) + r"\b", dlg, re.I):
                errors.append(
                    f"{where}: line voiced by {spk} mentions '{tok}' in third person — "
                    "this is narration; reassign to char_narrator")
                break
    for key in ("character", "place", "dialogue", "stage_directions"):
        if key not in line:
            errors.append(f"{where}: line missing key '{key}'")
    if line.get("character") not in char_ids:
        errors.append(f"{where}: unknown character '{line.get('character')}'")
    if line.get("place") not in place_ids:
        errors.append(f"{where}: unknown place '{line.get('place')}'")
    elif allowed_places is not None and line.get("place") not in allowed_places:
        errors.append(f"{where}: place '{line.get('place')}' is not one of this episode's places "
                      f"({sorted(allowed_places)})")
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


def validate_episode(ep, ep_id, char_ids, place_ids, assigned_tags, name_map,
                     anchors=None, allowed_places=None):
    errors = []
    if not isinstance(ep, dict):
        return ["top-level JSON is not an object"]
    if ep.get("id") != ep_id:
        errors.append(f"id is {ep.get('id')!r}, expected {ep_id!r}")
    acts = ep.get("acts")
    if not isinstance(acts, list) or len(acts) != 4:
        return errors + [f"acts must be a list of 4 (got {len(acts) if isinstance(acts, list) else type(acts).__name__})"]

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
                    validate_line(line, char_ids, place_ids, name_map, f"{sw} line {li+1}", errors, allowed_places)
                    dlg = (line.get("dialogue") or "").strip()
                    sd0 = (line.get("stage_directions") or "").strip().lower()
                    if "*" in dlg or "*" in sd0:
                        errors.append(f"{sw} line {li+1}: markdown asterisk in shipped text")
                    if sd0 and re.fullmatch(r"(asks?|asked|responds?|responded|repl(y|ies|ied)|frowns?|"
                                            r"sighs?|nods?|smiles?|says|said|murmurs?|whispers?|pauses?|"
                                            r"continues?|adds?)", sd0):
                        errors.append(f"{sw} line {li+1}: junk stage direction [{sd0}] restates the "
                                      "speech act — physical content or empty")
                    if line.get("character") == "char_narrator" and re.search(
                            r"\b(forged|forgery|fake|stolen)\b", dlg, re.I):
                        errors.append(f"{sw} line {li+1}: narrator uses spoiler word "
                                      "(forged/fake/stolen) for an unrevealed fact")
                    if line.get("character") == "char_narrator" and (
                            '"' in dlg or "“" in dlg or "”" in dlg or
                            re.search(r"\b(asks|says|said|replies|replied|answers|whispers|shouts|murmurs)\b",
                                      dlg, re.I)):
                        errors.append(f"{sw} line {li+1}: narrator line carries quoted/narrated speech "
                                      "— speech belongs to the speaking character (actions go in "
                                      "stage_directions)")
                    all_dialogue.append((dlg, f"{sw} line {li+1}"))
                    full_name_problems_into(dlg, name_map, f"{sw} line {li+1}", errors)
                    sd = (line.get("stage_directions") or "").strip()
                    full_name_problems_into(sd, name_map, f"{sw} line {li+1} stage_directions", errors)
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
                # the LAST line of the immediately preceding narrative segment
                # must use this tag's English anchor word
                if anchors and tid in anchors and si > 0:
                    word = anchors[tid][0] if isinstance(anchors[tid], tuple) else anchors[tid]
                    prev = segs[si - 1]
                    prev_lines = prev.get("lines", []) if isinstance(prev, dict) else (prev if isinstance(prev, list) else [])
                    last = (prev_lines[-1].get("dialogue") or "") if prev_lines else ""
                    if word and not re.search(r"\b" + re.escape(word) + r"\b", last, re.I):
                        errors.append(f"{sw}: the line immediately before tag '{tid}' does not use its "
                                      f"English anchor word {word!r} (last line: {last[:70]!r})")

        # decision
        dec = act.get("decision")
        if not isinstance(dec, dict):
            errors.append(f"{where}: missing decision object")
            continue
        validate_line(dec.get("line", {}), char_ids, place_ids, name_map, f"{where} decision.line", errors, allowed_places)
        dd = ((dec.get("line") or {}).get("dialogue") or "").strip()
        if dd:
            all_dialogue.append((dd, f"{where} decision.line"))
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
                validate_line(out.get("line", {}), char_ids, place_ids, name_map, lw, errors, allowed_places)
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
    # HARD GATE: zero Thai Unicode anywhere in the episode JSON — the story
    # must never give away the frontend's vocab quiz
    thai_hits = re.findall(r"[฀-๿]+", json.dumps(ep, ensure_ascii=False))
    if thai_hits:
        errors.append(f"HARD: episode JSON contains Thai text ({thai_hits[0][:20]}..., "
                      f"{len(thai_hits)} run(s)) — zero Thai allowed anywhere")
    return errors


def full_name_problems_into(text, name_map, where, errors):
    for p in full_name_problems(text, name_map, where):
        errors.append(p)


def _norm_text(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def transcription_problems(prose, ep, limit=15):
    """The formatter is a transcriber: every dialogue string and choice
    description in the JSON must be traceable to the prose. Flag any string
    that does not appear in the prose (formatter-invented content)."""
    norm_prose = _norm_text(re.sub(r"^\s*\[\[\s*tag_\d+\s*\]\]\s*$", "", prose, flags=re.M))
    problems = []

    def _walk(o, where):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("dialogue", "description") and isinstance(v, str) and v.strip():
                    nv = _norm_text(v).strip('"').strip()
                    if nv and nv not in norm_prose:
                        problems.append(f"{where}: {k} not found in the prose (formatter-invented or "
                                        f"rewritten): {v[:70]!r}")
                else:
                    _walk(v, where)
        elif isinstance(o, list):
            for v in o:
                _walk(v, where)

    for i, act in enumerate(ep.get("acts", []) if isinstance(ep, dict) else []):
        _walk(act.get("segments", []), f"act {i+1}")
        _walk(act.get("decision", {}), f"act {i+1} decision")
    return problems[:limit]


# ---------------------------------------------------------------- stages
def run_stage_once(usage, label, model, temperature, max_tokens, template_path,
                   slots, checker):
    """Generate once, check once. Returns (text, problems). Never re-prompts."""
    template = read_file(template_path)
    system, user = split_sys_user(fill(template, slots))
    log(f"[{label}] single generation call")
    text, _ = call_llm(model, system, user, temperature, max_tokens, usage, label)
    problems = checker(text) if checker else []
    if problems:
        log(f"[{label}] GATE FAILED ({len(problems)} problem(s) — recorded, continuing without regeneration):\n  - "
            + "\n  - ".join(problems))
    else:
        log(f"[{label}] passed gate")
    return text, problems


def spot_edit(usage, model, artifact, problems, label, max_tokens):
    """One editor pass: artifact + specific problem list -> fixed artifact.
    Never loops; caller re-gates once and records whatever remains."""
    if not problems:
        return artifact
    user = ("Here is a text with specific problems.\n\nPROBLEMS (with quoted contexts):\n- "
            + "\n- ".join(problems)
            + "\n\nRewrite ONLY the sentences/lines implicated above; keep every other line "
              "identical. Output the complete corrected text, nothing else.\n\nTEXT:\n" + artifact)
    log(f"[{label}] one spot-edit pass ({len(problems)} problem(s) to fix)")
    text, _ = call_llm(model, "You are a careful line editor.", user, 0.3,
                       max_tokens, usage, label)
    return text


# ---------------------------------------------------------------- decisions
DECISION_OPTION_RE = re.compile(
    r"\[(easy|medium|hard)\]\s*(.*?)\s*\((attr_\w+)\)\s*"
    r"PASS:\s*[\"“](.*?)[\"”]\s*FAIL:\s*[\"“](.*?)[\"”](?=\s*/\s*\[|\s*$)", re.S)
DECISION_HEAD_RE = re.compile(
    r"DECISION\s*—\s*dilemma line\s*\(([^)]+)\):\s*[\"“](.*?)[\"”]", re.S)


def parse_decisions(plan, name_map):
    """Extract per-act decision content from the outline's DECISION beats.
    Returns {act_num: {"speaker": char_id|None, "dilemma": str,
                       "choices": [{difficulty, description, attribute, pass, fail}]}}"""
    out = {}
    for anum, body in _act_sections(plan):
        for n, t in _beats(body):
            if not t.upper().startswith("DECISION"):
                continue
            head = DECISION_HEAD_RE.search(t)
            options = DECISION_OPTION_RE.findall(t)
            speaker = None
            if head:
                names = _names_in(head.group(1), name_map)
                speaker = sorted(names)[0] if names else None
            choices = [{"difficulty": d, "description": opt.strip(),
                        "attribute": at, "pass": p.strip(), "fail": f.strip()}
                       for d, opt, at, p, f in options]
            out[anum] = {"speaker": speaker,
                         "dilemma": head.group(2).strip() if head else "",
                         "choices": choices}
    return out


# ---------------------------------------------------------------- deterministic formatter
def format_episode(prose, plan, ep_id, tag_ids, name_map, char_ids, places_json,
                   allowed_place_ids):
    """Pure-Python formatter. No LLM. The prose contract (see prompts/prose.md):
      ## Act N — Title
      PLACE: <place name>
      NARRATOR: <sentence>
      <Nickname>: "<speech>"  (marker [[tag_xxx]] may trail any line)
    Decisions come VERBATIM from the plan's DECISION beats.
    Returns (ep, errors, fatal). fatal = unmappable content (never invent)."""
    errors, fatal = [], []

    # name lookup: nickname/full name (and "The "-stripped variants) -> char id
    lookup = {}
    for cid, (full, nick) in name_map.items():
        for nm in {full, nick} - {None}:
            lookup[nm.lower()] = cid
            if nm.lower().startswith("the "):
                lookup[nm[4:].lower()] = cid
    lookup["narrator"] = "char_narrator"
    place_lookup = {}
    for p in places_json:
        nm = (p.get("name") or "").strip()
        if nm:
            place_lookup[nm.lower()] = p["id"]
            if nm.lower().startswith("the "):
                place_lookup[nm[4:].lower()] = p["id"]
        place_lookup[p["id"]] = p["id"]

    decisions = parse_decisions(plan, name_map)

    # split into acts
    parts = re.split(r"^#{1,3}\s+Act\s+([1-4])\b[^\n]*$", prose, flags=re.M)
    act_bodies = {}
    for i in range(1, len(parts) - 1, 2):
        act_bodies[int(parts[i])] = parts[i + 1]
    if sorted(act_bodies) != [1, 2, 3, 4]:
        fatal.append(f"prose does not have exactly acts 1-4 (found {sorted(act_bodies)})")
        return None, errors, fatal

    acts = []
    used_tags = []
    for anum in (1, 2, 3, 4):
        where = f"act {anum}"
        body = act_bodies[anum]
        title_m = re.search(r"^#{1,3}\s+Act\s+%d\b\s*[—:-]?\s*(.*)$" % anum, prose, re.M)
        title = (title_m.group(1).strip() if title_m and title_m.group(1).strip() else f"Act {anum}")
        pm = re.search(r"^PLACE:\s*(.+?)\s*$", body, re.M)
        if not pm:
            fatal.append(f"{where}: no PLACE: line")
            continue
        place = place_lookup.get(pm.group(1).strip().lower())
        if not place:
            # tolerant fallback: exactly one allowed place sharing a significant
            # token with the given name ("veranda of the canal-side school" ->
            # "The School Veranda")
            tokens = {w for w in re.findall(r"[a-z]{4,}", pm.group(1).lower())}
            cands = {pid for name, pid in place_lookup.items()
                     if pid in allowed_place_ids and tokens & set(re.findall(r"[a-z]{4,}", name))}
            if len(cands) == 1:
                place = cands.pop()
                log(f"[format] {where}: PLACE {pm.group(1).strip()!r} fuzzy-mapped to {place}")
        if not place:
            fatal.append(f"{where}: PLACE {pm.group(1).strip()!r} does not map to any known place id")
            continue
        if place not in allowed_place_ids:
            errors.append(f"{where}: place {place} is not one of this episode's places "
                          f"({sorted(allowed_place_ids)})")
        # content lines: stop at a DECISION block if the writer emitted one
        body = re.split(r"^DECISION:?\s*$", body, flags=re.M)[0]
        lines, tags_here = [], []
        for raw in body.splitlines():
            raw = raw.strip()
            if not raw or raw.startswith("#") or raw.upper().startswith("PLACE:"):
                continue
            pending_tag = None
            tm = TAG_MARKER_RE.search(raw)
            if tm:
                raw = TAG_MARKER_RE.sub("", raw).strip()
                pending_tag = tm.group(1)
            if not raw:
                if pending_tag:
                    tags_here.append((pending_tag, len(lines)))
                continue
            sm = re.match(r"^([^:]{1,40}?):\s+(.*)$", raw, re.S)
            if not sm:
                fatal.append(f"{where}: line has no 'Speaker:' prefix: {raw[:70]!r}")
                continue
            who, text = sm.group(1).strip(), sm.group(2).strip()
            cid = lookup.get(who.lower())
            if cid is None:
                fatal.append(f"{where}: speaker {who!r} does not map to any character id")
                continue
            if cid not in char_ids:
                fatal.append(f"{where}: speaker {who!r} maps to unknown id {cid}")
                continue
            stage = ""
            tm2 = re.match(r"^\[(.+?)\]\s*(.*)$", text.strip(), re.S)
            if tm2:
                stage, text = tm2.group(1).strip(), tm2.group(2).strip()
            dlg = text.strip()
            if len(dlg) >= 2 and dlg[0] in "\"“" and dlg[-1] in "\"”":
                dlg = dlg[1:-1]
            if not dlg and not stage:
                fatal.append(f"{where}: empty line for speaker {who!r}")
                continue
            lines.append({"character": cid, "place": place, "dialogue": dlg,
                          "stage_directions": stage})
            if pending_tag:
                tags_here.append((pending_tag, len(lines)))  # tag AFTER this line
        # split at markers into 3 narrative groups + 2 tags
        if len(tags_here) != 2:
            fatal.append(f"{where}: found {len(tags_here)} tag markers (need exactly 2)")
            continue
        (t1, i1), (t2, i2) = tags_here
        used_tags.extend([t1, t2])
        # FORMATTER HONESTY (PO directive): the formatter never merges,
        # reorders, or repositions anything. Any segment outside contract —
        # too few OR too many lines, including 1-line segments — is FATAL:
        # no JSON, loud report. The repair path is the prose spot-edit.
        seg1 = lines[:i1]
        seg3 = lines[i1:i2]
        seg5 = lines[i2:]
        if not (8 <= len(lines) <= 12):
            fatal.append(f"{where}: act has {len(lines)} lines (contract: 8-12)")
        for seg, lo, hi, sname in ((seg1, 4, 6, "segment 1"), (seg3, 2, 3, "segment 3"),
                                   (seg5, 2, 3, "segment 5")):
            if not (lo <= len(seg) <= hi):
                fatal.append(f"{where} {sname}: has {len(seg)} lines (contract {lo}-{hi}) — "
                             "FATAL; the prose spot-edit is the only repair path")
        segments = [
            {"type": "narrative", "lines": seg1},
            {"type": "tag", "tag": t1},
            {"type": "narrative", "lines": seg3},
            {"type": "tag", "tag": t2},
            {"type": "narrative", "lines": seg5},
        ]
        # decision from the PLAN, verbatim
        dec = decisions.get(anum)
        if not dec or len(dec["choices"]) != 3:
            errors.append(f"{where}: plan has no complete DECISION beat "
                          f"({len(dec['choices']) if dec else 0}/3 choices parsed)")
            decision = None
        else:
            speaker = dec["speaker"] or "char_pricha"
            # the dilemma line must be NEW — not a verbatim repeat of any
            # narrative line in this act
            if dec["dilemma"] and any(dec["dilemma"] == l["dialogue"] for l in lines):
                errors.append(f"{where}: decision.line verbatim-duplicates a narrative line — "
                              "the dilemma must be written as a new line (or the prose occurrence "
                              "suppressed)")
            decision = {
                "line": {"character": speaker, "place": place,
                         "dialogue": dec["dilemma"], "stage_directions": ""},
                "choices": [{
                    "description": c["description"],
                    "difficulty": c["difficulty"],
                    "attribute": c["attribute"],
                    "pass_outcome": {"line": {"character": "char_pricha", "place": place,
                                              "dialogue": c["pass"], "stage_directions": ""},
                                     "attribute": c["attribute"], "delta": 1},
                    "fail_outcome": {"line": {"character": "char_pricha", "place": place,
                                              "dialogue": c["fail"], "stage_directions": ""},
                                     "attribute": c["attribute"], "delta": 0},
                } for c in dec["choices"]],
            }
        acts.append({"id": f"act_{anum}", "title": title,
                     "segments": segments, "decision": decision})

    if sorted(used_tags) != sorted(tag_ids):
        errors.append(f"tags used {sorted(used_tags)} != assigned set {sorted(tag_ids)}")
    if fatal:
        return None, errors, fatal
    title = acts[-1]["title"] if acts else ep_id
    ep_out = {"id": ep_id, "title": title, "acts": acts}
    return ep_out, errors, fatal


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


def normalize_episode(ep, ep_id):
    """Metadata-only structural fixes. Never rewrites content."""
    if not isinstance(ep, dict):
        return ep
    ep["id"] = ep_id
    acts = ep.get("acts") or []
    for a in acts:
        if isinstance(a, dict) and isinstance(a.get("segments"), list):
            a["segments"] = [
                {"type": "narrative", "lines": s} if isinstance(s, list) else s
                for s in a["segments"]]
    if ep.get("title") in (None, "", "Sticky Situation") and acts:
        ep["title"] = acts[-1].get("title") or ep_id
    return ep


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(
        description="Single-pass 3-stage episode pipeline (plan -> prose -> format). "
                    "Each stage runs once; gate failures are recorded in the report, never retried.")
    ap.add_argument("--ep-id", required=True)
    ap.add_argument("--foreground", required=True, help="foregrounded character id, e.g. char_sangwan")
    ap.add_argument("--places", required=True, help="comma-separated place ids (foregrounded locations)")
    ap.add_argument("--tags", required=True, help="comma-separated 8 tag ids")
    ap.add_argument("--model-plan", required=True)
    ap.add_argument("--model-prose", required=True)
    ap.add_argument("--model-edit", required=True, help="model for spot-edit passes")
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    shortlist = [t.strip() for t in args.tags.split(",") if t.strip()]
    if len(shortlist) != 12:
        raise SystemExit("exactly 12 shortlist tag ids required (the planner picks 8)")
    place_ids = [p.strip() for p in args.places.split(",") if p.strip()]

    usage = Usage()
    gate_results = {}  # stage -> list of problems

    # ----- load inputs
    shared = read_file(os.path.join(WORLD_DIR, "shared_context.md"))
    char_ids = {c["id"] for c in load_json(os.path.join(REPO_PUBLIC, "characters.json"))}
    place_id_set = {p["id"] for p in load_json(os.path.join(REPO_PUBLIC, "places.json"))}
    name_map = build_name_map()

    # Public character texts go to every stage. The foregrounded character's
    # PRIVATE plan goes ONLY to the planner: secrets are planned around, never
    # passed downstream to the writer/formatter.
    char_texts = [load_character_text("char_pricha"), load_character_text(args.foreground)]
    fg_text = char_texts[1]
    for cid in sorted(char_ids):
        if cid in fg_text and cid not in ("char_pricha", args.foreground, "char_narrator"):
            char_texts.append(load_character_text(cid))
    private_text = load_private_text(args.foreground)
    place_texts = [load_place_text(pid) for pid in place_ids]
    place_texts.append(load_place_text("place_veranda"))

    # allowed places: the episode's --places plus the veranda, nothing else
    allowed_place_ids = set(place_ids) | {"place_veranda"}
    # place private plans feed the planner only (dialectical phrase pool)
    place_private_text = "\n\n".join(
        load_private_text(pid) for pid in sorted(allowed_place_ids - {"place_veranda"})
        if os.path.exists(os.path.join(PRIVATE_DIR, pid + "_private.md")))
    places_json = load_json(os.path.join(REPO_PUBLIC, "places.json"))
    all_place_names = {(p.get("name") or "").strip() for p in places_json} - {""}
    allowed_place_names = {(p.get("name") or "").strip() for p in places_json
                           if p.get("id") in allowed_place_ids} - {""}

    slots = {
        "SHARED_CONTEXT": shared,
        "CHARACTER_FILES": "\n\n".join(char_texts),
        "PLACE_FILES": "\n\n".join(place_texts),
        "EP_ID": args.ep_id,
        "TAGS_WITH_NAMES": resolve_tags(shortlist),
        "FOREGROUNDED": args.foreground,
        "NICKNAMES": nickname_guide(name_map),
        "ALLOWED_PLACES": "\n".join(f"- {p['id']} ({(p.get('name') or '').strip()})"
                                    for p in places_json if p.get("id") in allowed_place_ids),
        "PRIVATE_PLAN": private_text or "(no private plan on file — invent nothing secret; work from the public file only)",
    }
    global ALLOWED_PLACES_TEXT
    ALLOWED_PLACES_TEXT = "\n".join(f"- {(p.get('name') or '').strip()}"
                                    for p in places_json if p.get("id") in allowed_place_ids)

    # ----- STAGE 1: atomic plan decomposition (4 incremental calls, one
    # instruction each) then gate, then ONE spot-edit pass if needed.
    plan_checker = lambda t: check_plan(t, shortlist, name_map,
                                        allowed_place_names, all_place_names)
    # step 1: base outline (full context)
    plan, _ = run_stage_once(
        usage, "plan-1-base", args.model_plan, 0.7, 8000,
        os.path.join(PROMPTS_DIR, "plan.md"), slots, None)
    # steps 2-5: small additive edits (outline + one instruction each)
    step_template = read_file(os.path.join(PROMPTS_DIR, "plan_step.md"))
    step_instructions = [
        ("plan-2-stakes-entrances",
         "Give the outline back with these additions, changing nothing else:\n"
         "(1) In Act 1, add one early beat (beats 1-6, machine-checked) labeled 'STAKES:' in which "
         "a character says aloud, in quoted words, what they want AND the concrete cost if they "
         "fail. Required sentence shape: '<want>, or <concrete cost>' — the word 'or' (or "
         "'otherwise'/'if not') followed by the named cost is machine-checked.\n"
         "(2) For every character in Act 1's PRESENT line whose presence is NOT obvious from the "
         "place (a clerk in a salt store IS obvious — no introduction needed; a stranger in a salt "
         "store is NOT), insert an 'ENTRANCE <nickname>:' beat within the first 6 beats (who they "
         "are, what they are doing, what they carry) BEFORE that character's first speech beat. "
         "Do the same for any character who first appears in a later act. Nobody may be revealed "
         "present late if they would obviously have been noticed from the start.\n"
         "(2b) Make sure every Act 1 beat is LOADED — append to each its annotation "
         "'— carries: intro:<nickname>, setting, stakes, thesis, deadline, ...' listing the plan "
         "elements it carries; merge single-purpose beats so no run of 3 survives."
         "(3) Fix the opening stretch so that at most the PC plus ONE other character speaks in the "
         "first 6 beats — move other speakers' beats later if needed.\n"
         "(4) If any beat plants a deadline (a date, 'by noon', 'the mail boat'), make sure Act 3 "
         "has a beat where that deadline converges (it arrives, is nearly missed, or forces a "
         "choice)."),
        ("plan-3-decisions",
         "Give the outline back with ONE DECISION beat added at the end of EACH act, changing "
         "nothing else. Exact shape (machine-parsed):\n"
         "N. DECISION — dilemma line (<nickname of a character present>): \"<dilemma>\" / "
         "[easy] <concrete action, 10-20 words> (attr_x) PASS: \"I ...\" FAIL: \"I ...\" / "
         "[medium] ... / [hard] ...\n"
         "Rules: each option is 10-20 words, concrete, and uses ONLY objects/facts/people already "
         "established in the beats of this or earlier acts; attr_x is one of attr_heart_water, "
         "attr_deference, attr_ledger, attr_word_hoard, attr_merit_water; PASS and FAIL are the PC "
         "speaking in first person — EVERY one of the six texts begins with the word 'I' "
         "(machine-checked) — each ONE concrete event visibly resulting from THAT option's "
         "action and naming the scene's objects; PASS and FAIL differ. The dilemma line is "
         "IN-CHARACTER dialogue: the named character reacting to THIS situation in their own voice "
         "(a clerk frets about his ledger; a boatman talks weather). The four dilemma lines of the "
         "episode must NOT share a template — no two may open with the same three words."),
        ("plan-4-machinery",
         "Give the outline back with three kinds of beats added or marked, changing nothing else. "
         "Each is a LABEL plus concrete content — never explain what the label means:\n"
         "(1) THESIS: Draw dialectical noun phrases from the foregrounded character's private "
         "material AND the place's private material below — use at least 2 DISTINCT phrases when "
         "the private plans provide them; do NOT coin new phrases when they do. Style: direct "
         "apposition, no 'like'/'as if' ('of' is fine: 'the letter-writer, clerk of other people's "
         "news'). Write them into the outline as 'THESIS \"<phrase>\":' beats: act-1 beat 1 (the "
         "opening line must use one) plus at least 2 later occurrences in different acts. NO phrase "
         "may appear on more than 2 beats — vary which phrase a beat carries.\n"
         "PLACE PRIVATE MATERIAL (phrase pool, planner-only):\n" + (place_private_text or "(none)") + "\n"
         "(2) REFRAIN: Write one short line of exact wording and place it at 3 occurrences spread "
         "across at least 2 acts, each a beat 'REFRAIN \"<wording>\": <how its meaning changes in "
         "this context>'. The three occurrences must NEVER be verbatim twice — each rewords the "
         "refrain's core words. The final occurrence must be cosmic in scale (sky/sea/stars/the "
         "turning world) while echoing those core words.\n"
         "(3) WONDER: one beat per act labeled 'WONDER (<shape>):' where <shape> is one of "
         "inventory / numinous / connoisseur / elegiac, followed by the concrete content: for "
         "inventory, supply the actual numbers or taxonomy; for numinous, a marvel everyone "
         "treats calmly; for connoisseur, a character's disciplined seeing; for elegiac, "
         "foreknowledge that this world is passing. Any comparison inside a WONDER beat must come "
         "from the story's own material."),
("plan-5-tags",
         "Give the outline back with a '## TAG PLAN' section appended and the tag beats marked, "
         "changing nothing else. The story contains NO Thai anywhere — the link between story and "
         "tag is ENTIRELY IN ENGLISH: the line immediately before each tag uses the English word "
         "that best unifies the tag's theme, and the surrounding lines evoke that theme in English.\n"
         "THE 12-TAG SHORTLIST (use these exact ids, nothing else):\n" + resolve_tags(shortlist) + "\n"
         "From this shortlist, PICK the 8 tags whose themes this "
         "episode's situations can best evoke, and assign 2 per act. For each picked tag add one "
         "bullet EXACTLY of this shape (machine-parsed):\n"
         "- tag_xxx — English anchor word: \"<one ordinary English word that best unifies the tag's "
         "theme; all 8 words different>\" — act N, position 1|2 — beat it attaches to: <one clause>\n"
         "For each tag, adjust that act's beats so there is a pair of ADJACENT beats:\n"
         "- FIRST beat, prefixed 'TAG tag_xxx:' — the THEME SCENE: a concrete situation in which "
         "the tag's theme is alive (for a hearing tag: someone strains to catch the words behind "
         "the wall). English only.\n"
         "- SECOND beat — a dramatic REACTION: an action or reply that MOVES THE SCENE (never an "
         "explanation, never 'showing X' / 'ignoring Y'). Its sentence carries the tag's English "
         "anchor word and becomes the last line before the tag.\n"
         "BEAT BUDGET per act (machine-checked by counting your numbered beats): one beat = one "
         "prose line, so the act's beat counts ARE the segment line counts: the beats up to and "
         "including the FIRST tag's reaction beat must number 4–6 (segment 1); the beats between "
         "the two tags' reaction beats must number 2–3 (segment 3); the beats after the second "
         "tag's reaction must number 2–3 (segment 5). Total 8–12 content beats per act, plus the "
         "DECISION beat (which the writer never expands). If a stretch is too long, MERGE beats "
         "here in the outline — never leave the writer more beats than the budget. Number your "
         "beats so this lands."),
            ]
    for label, instruction in step_instructions:
        step_filled = fill(step_template, {"OUTLINE": plan, "STEP_INSTRUCTION": instruction,
                                           "NICKNAMES": slots["NICKNAMES"]})
        system, user = split_sys_user(step_filled)
        log(f"[{label}] single generation call")
        plan, _ = call_llm(args.model_plan, system, user, 0.4, 8000, usage, label)

    plan_problems = plan_checker(plan)
    gate_results["plan (before spot-edit)"] = plan_problems
    if plan_problems:
        log(f"[plan] GATE FAILED ({len(plan_problems)} problem(s)) — one spot-edit pass follows")
        edit_problems = plan_problems + [
            "REFERENCE — the only valid tag ids (the 12-tag shortlist): " + ", ".join(shortlist),
            "HARD RULE: beats labeled THESIS / REFRAIN / WONDER are UNTOUCHABLE — never delete, "
            "move, or reword them, no matter what the other fixes require."]
        mach = lambda ps: [p for p in ps if any(k in p.lower() for k in ("thesis", "refrain", "wonder"))]
        fatal_cls = lambda ps: [p for p in ps if "no beat labeled 'STAKES:'" in p
                                or "STAKES beat names no concrete cost" in p
                                or "TAG PLAN must pick exactly 8" in p
                                or "missing mandatory section header" in p
                                or "OUTLINE must have '### Act 1'" in p]
        edited = spot_edit(usage, args.model_edit, plan, edit_problems, "plan-spot-edit", 24000)
        edited_problems = plan_checker(edited)
        # weighted keep-better guard: an edit is DISQUALIFIED if it introduces
        # ANY machinery-gate failure or increases a FATAL class — even when
        # the total count drops. One retry is allowed ONLY to restore
        # stripped machinery beats.
        if mach(edited_problems) and not mach(plan_problems):
            log("[plan] spot-edit STRIPPED machinery beats — one retry to restore them verbatim")
            edited2 = spot_edit(usage, args.model_edit, edited,
                                edited_problems + ["Restore the THESIS/REFRAIN/WONDER beats "
                                                   "VERBATIM from the previous version; they are untouchable."],
                                "plan-spot-edit-restore", 16000)
            e2p = plan_checker(edited2)
            if not (mach(e2p) and not mach(plan_problems)):
                edited, edited_problems = edited2, e2p
        disqualified = (mach(edited_problems) and not mach(plan_problems)) or \
                       len(fatal_cls(edited_problems)) > len(fatal_cls(plan_problems))
        if not disqualified and len(edited_problems) < len(plan_problems):
            plan, plan_problems = edited, edited_problems
            log(f"[plan] after spot-edit: {len(plan_problems)} problem(s) remain — recorded, continuing")
        else:
            why = "disqualified (machinery stripped / FATAL class grew)" if disqualified else \
                  f"would leave {len(edited_problems)} problems vs {len(plan_problems)} before"
            log(f"[plan] spot-edit DISCARDED ({why}) — keeping the original, failures recorded")
        gate_results["plan (after spot-edit)"] = plan_problems
    else:
        log("[plan] passed gate")
    # STAKES is a hard contract: if the spot-edit could not produce a costed
    # STAKES beat, the episode has no engine — fail loudly, do not continue
    stakes_fatal = [p for p in plan_problems
                    if "no beat labeled 'STAKES:'" in p or "STAKES beat names no concrete cost" in p]
    if stakes_fatal:
        gate_results["plan FATAL"] = stakes_fatal
        log("[plan] FATAL: no costed STAKES beat after spot-edit — aborting episode")
        ep = None
        anchors = {}
    # the planner's chosen 8 tags drive everything downstream; without a
    # parseable set of 8, downstream is meaningless — FATAL like STAKES
    picked, picked_acts = extract_picked_tags(plan)
    tags_fatal = stakes_fatal or len(picked) != 8
    if len(picked) != 8 and not stakes_fatal:
        gate_results["plan FATAL"] = [f"TAG PLAN did not yield exactly 8 parseable shortlist tags "
                                      f"(got {len(picked)}) — cannot assign markers downstream"]
        log(f"[plan] FATAL: planner picked {len(picked)} tags (need 8 from the shortlist) — aborting")
    anchors = extract_english_anchors(plan) if not tags_fatal else {}
    tag_ids = picked
    unused_shortlist = [t for t in shortlist if t not in picked]

    # ----- STAGE 2: prose, PER ACT (4 calls; monolithic generation is
    # physically impossible for v4-flash with the annotated plans).
    # Each act gets: full outline (coherence), its own 2-tag checklist, a
    # mechanical carryover (the previous act's last lines). Each act is
    # gated on arrival; a FATAL-class failure retries ONLY that act once.
    prose = ""
    ep = None
    if not tags_fatal:
        act_texts = {}
        carryover = "(this is Act 1 — no prior acts; it opens the episode)"
        # sprint-5 pass-3 runtime levers: 16000 caps; reasoning=low (in
        # call_llm); temp-0.6 on transport failure; qwen fallback for
        # prose+edit if v4-flash stays untransportable
        act_tmpl = os.path.join(PROMPTS_DIR, "prose_act.md")
        prose_model = [args.model_prose]
        edit_model = [args.model_edit]
        QWEN = "qwen/qwen3-235b-a22b-2507"

        def gen_act(label, slots, checker):
            try:
                return run_stage_once(usage, label, prose_model[0], 0.8, 16000,
                                      act_tmpl, slots, checker)
            except RuntimeError:
                log(f"[{label}] transport failure at temp 0.8 — lever 3: temp 0.6 retry")
            try:
                return run_stage_once(usage, label + "-t0.6", prose_model[0], 0.6, 16000,
                                      act_tmpl, slots, checker)
            except RuntimeError:
                if prose_model[0] != QWEN:
                    log(f"[{label}] v4-flash untransportable — lever 4: PROSE+EDIT fall back to "
                        f"{QWEN} (sprint-1 stable; regression risk logged)")
                    prose_model[0] = edit_model[0] = QWEN
                return run_stage_once(usage, label + "-qwen", prose_model[0], 0.6, 16000,
                                      act_tmpl, slots, checker)

        def edit_act(label, text, aprobs, checker):
            try:
                return spot_edit(usage, edit_model[0], text, aprobs, label, 16000)
            except RuntimeError as te:
                log(f"[{label}] transport failure ({te}) — keeping text")
                return None

        for anum in (1, 2, 3, 4):
            act_tags = [t for t in tag_ids if picked_acts.get(t) == anum]
            cheat = "\n".join(
                f"- [[{tid}]] — English anchor word \"{anchors.get(tid, '?')}\" in the line "
                "IMMEDIATELY before the marker; the lines before it evoke the tag's theme "
                "IN ENGLISH (no Thai)." for tid in act_tags)
            act_slots = {
                "PLAN": plan,
                "NICKNAMES": slots["NICKNAMES"],
                "EP_ID": args.ep_id,
                "ANCHOR_CHEAT": cheat,
                "ALLOWED_PLACES": slots["ALLOWED_PLACES"],
                "ACT_NUM": str(anum),
                "CARRYOVER": carryover,
            }
            act_checker = lambda t, a=anum, tg=act_tags: check_prose_act(t, a, plan, tg, name_map)
            fatal_cls = re.compile(r"no 'PLACE:'|not one of the allowed|maps to no character|"
                                   r"tag markers|prose lines \(expected|could not split|"
                                   r"contract 8-12")
            text, aprobs = gen_act(f"prose-act{anum}", act_slots, act_checker)
            gate_results[f"prose act {anum} (before spot-edit)"] = aprobs
            for attempt in (1, 2):  # one spot-edit; then ONE act-only retry if FATAL-class remains
                if aprobs:
                    edited = edit_act(f"prose-act{anum}-spot-edit", text, aprobs, act_checker)
                    if edited:
                        eprobs = act_checker(edited)
                        if len(eprobs) < len(aprobs):
                            text, aprobs = edited, eprobs
                    gate_results[f"prose act {anum} (after spot-edit)"] = aprobs
                if not any(fatal_cls.search(p) for p in aprobs) or attempt == 2:
                    break
                log(f"[prose-act{anum}] FATAL-class failures remain — ONE act-only retry")
                text2, p2 = gen_act(f"prose-act{anum}-retry", act_slots, act_checker)
                if len(p2) <= len(aprobs):
                    text, aprobs = text2, p2
                gate_results[f"prose act {anum} (retry)"] = aprobs
            act_texts[anum] = text
            # mechanical carryover: the act's last content lines glue the next
            # act's opening
            clines = [ln.strip() for ln in text.splitlines()
                      if ln.strip() and not ln.strip().startswith("#")
                      and not ln.strip().upper().startswith("PLACE:")]
            tail = " / ".join(ln[:160] for ln in clines[-2:]) if clines else "(act ended empty)"
            carryover = f"Act {anum} ended: {tail}"
            log(f"[prose-act{anum}] done: {len(aprobs)} problem(s)")
        prose = "\n\n".join(act_texts[a] for a in (1, 2, 3, 4))
        prose_problems = check_prose(prose, plan, tag_ids, name_map)
        gate_results["prose (assembled, full-document checks)"] = prose_problems
        # checkpoint intermediates immediately (crash safety)
        try:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
            with open(args.out + ".plan.md", "w", encoding="utf-8") as fh:
                fh.write(plan)
            with open(args.out + ".prose.md", "w", encoding="utf-8") as fh:
                fh.write(prose)
        except Exception as ce:
            log(f"[checkpoint] could not save intermediates: {ce}")

        # ----- STAGE 3: deterministic formatter (no LLM)
        ep, fmt_errors, fmt_fatal = format_episode(prose, plan, args.ep_id, tag_ids,
                                                   name_map, char_ids, places_json,
                                                   allowed_place_ids)
        if fmt_fatal:
            gate_results["format"] = [f"FATAL: {f}" for f in fmt_fatal] + fmt_errors
            log(f"[format] FATAL ({len(fmt_fatal)} unmappable item(s)) — no episode written:\n  - "
                + "\n  - ".join(fmt_fatal))
            ep = None
        else:
            anchors_full = {tid: (anchors.get(tid), None) for tid in tag_ids}
            fmt_errors += validate_episode(ep, args.ep_id, char_ids, place_id_set,
                                           set(tag_ids), name_map, anchors_full,
                                           allowed_place_ids)
            gate_results["format"] = fmt_errors
            if fmt_errors:
                log(f"[format] GATE FAILED ({len(fmt_errors)} problem(s) — recorded, episode kept as-is):\n  - "
                    + "\n  - ".join(fmt_errors))
            else:
                log("[format] passed gate")
    else:
        gate_results.setdefault("prose", []).append("skipped: plan FATAL (no costed STAKES beat)")
        gate_results.setdefault("format", []).append("skipped: plan FATAL (no costed STAKES beat)")

    # ----- outputs
    status = "SUCCESS"
    if ep is None:
        status = "FAILED (hard contract violation — see report)"
    elif any(gate_results.values()):
        status = "COMPLETED WITH GATE FAILURES (see report)"

    if ep is not None:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(ep, f, ensure_ascii=False, indent=2)
        log(f"[out] wrote {args.out}")
        base, _ = os.path.splitext(args.out)
        for suffix, text in ((".plan.md", plan), (".prose.md", prose)):
            if text:
                with open(base + suffix, "w", encoding="utf-8") as f:
                    f.write(text)
                log(f"[out] wrote {base}{suffix}")

    report = []
    report.append(f"# Pipeline report — {args.ep_id}")
    report.append(f"- models: plan={args.model_plan}, prose={args.model_prose}, "
                  f"spot-edit={args.model_edit}, format=deterministic (no LLM)")
    report.append(f"- mode: atomic plan steps + single pass per stage + one spot-edit per stage, no loops")
    report.append(f"- tokens: prompt={usage.prompt}, completion={usage.completion}")
    report.append(f"- cost estimate: ${usage.cost:.4f} (MODEL_PRICES in driver.py; update per model)")
    report.append(f"- final status: {status}")
    report.append(f"- tags picked by planner: {', '.join(picked) or '(none parsed)'}")
    report.append(f"- shortlist tags NOT used (for PO balancing): {', '.join(unused_shortlist) or '(none)'}")
    report.append("\n## Gate results")
    for stage, probs in gate_results.items():
        if not probs:
            report.append(f"- {stage}: PASS")
        else:
            report.append(f"- {stage}: FAIL ({len(probs)} problem(s))")
            report.extend(f"  - {p}" for p in probs)
    report.append("\n## Log\n```")
    report.extend(log_lines)
    report.append("```")
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    log(f"[out] wrote {args.report}")

    if ep is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
