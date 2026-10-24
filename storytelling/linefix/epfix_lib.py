#!/usr/bin/env python3
"""Shared library for the episode line-fix pipeline.

Serializes episodes to numbered lines, renders LLM prompts, parses diffs,
applies patches, and validates episode structure.
"""
import json, re, sys

THAI_RE = re.compile(r'[\u0E00-\u0E7F]')

def iter_line_paths(ep):
    """Yield (path_tuple, line_dict) for every editable line in an episode."""
    for ai, act in enumerate(ep['acts']):
        for si, seg in enumerate(act['segments']):
            if seg['type'] == 'narrative':
                for li, line in enumerate(seg['lines']):
                    yield (ai, si, li), line
        dec = act.get('decision')
        if not dec:
            continue
        yield (ai, 'D', None), dec['line']
        for ci, ch in enumerate(dec.get('choices', [])):
            yield (ai, 'C', ci), ch
            yield (ai, 'P', ci), ch['pass_outcome']['line']
            yield (ai, 'F', ci), ch['fail_outcome']['line']

def line_id(ai, kind, idx):
    return f'a{ai}s{kind}' if idx is None else f'a{ai}s{kind}l{idx}'

def render_episode(ep, char_names):
    out = []
    for ai, act in enumerate(ep['acts']):
        out.append(f'== ACT {ai+1}: "{act["title"]}" ==')
        for si, seg in enumerate(act['segments']):
            if seg['type'] == 'tag':
                out.append(f'  [TAG SEGMENT: {seg["tag"]}]')
                continue
            budget = '4-6' if si == 0 else '2-3'
            out.append(f'  -- narrative segment {si} (budget {budget} lines) --')
            for li, line in enumerate(seg['lines']):
                lid = line_id(ai, si, li)
                out.append(format_line(lid, line, char_names))
        dec = act.get('decision')
        if dec:
            out.append(f'  -- decision line --')
            out.append(format_line(f'a{ai}sD', dec['line'], char_names))
            for ci, ch in enumerate(dec['choices']):
                out.append(f'  -- choice {ci+1} ({ch["difficulty"]}, attribute {ch["attribute"]}): description --')
                out.append(f'[{line_id(ai,"C",ci)}] CHOICE: "{ch["description"]}"')
                out.append(f'  -- choice {ci+1} pass outcome --')
                out.append(format_line(f'a{ai}sPl{ci}', ch['pass_outcome']['line'], char_names))
                out.append(f'  -- choice {ci+1} fail outcome --')
                out.append(format_line(f'a{ai}sFl{ci}', ch['fail_outcome']['line'], char_names))
    return '\n'.join(out)

def format_line(lid, line, char_names):
    spk = line['character']
    name = char_names.get(spk, spk)
    sd = line.get('stage_directions') or ''
    s = f'[{lid}] {spk} ({name}): "{line["dialogue"]}"'
    if sd:
        s += f'  <stage: {sd}>'
    return s

def build_prompt(ep, chars, places):
    char_names = {c['id']: c['name'] for c in chars}
    place_ids = ', '.join(sorted(p['id'] for p in places))
    cast = '\n'.join(f"- {c['id']} ({c['name']}, type={c['type']}): {c.get('description','')[:120]}"
                     for c in chars)
    body = render_episode(ep, char_names)
    hints = build_hints(ep)
    hint_block = ('## Lines flagged by automated checks — these MUST be fixed\n'
                  + '\n'.join(hints) + '\n\n') if hints else ''
    prompt = f'''You are a meticulous script editor for a narrative RPG. Below is one episode rendered as numbered lines.

## Valid speakers (dramatis personae — use these exact ids)
{cast}

## Valid place ids
{place_ids}

## Editing rules — fix ONLY these defect classes
1. Dialogue attributed to the wrong speaker, especially a character's spoken line given to char_narrator. Reassign to the correct speaker id. Do not invent new ids.
2. A single numbered line containing two fragments of dialogue from different speakers (often with stray asterisks or quotation marks between them). Split it: keep the first fragment on the original line id and put the second fragment on a new id obtained by appending "x" (e.g. a0s1l1x). The new line inherits the place and stage_directions of the original unless clearly wrong.
3. Non sequitur lines that do not fit the scene (e.g. the repeated line "A boat nudges its post and settles." appearing where no boat is present). Delete them with a DELETE op, unless deleting would break a segment's line budget (first narrative segment of an act must keep 4-6 lines, the other two 2-3 each); in that case rewrite the line minimally so it fits the scene instead.
4. Stage directions that are not physical actions (e.g. "space between breaths"). Replace them with a concrete physical action or empty them (use -).
5. Incomplete sentences (e.g. "It is a difference of ."). Complete them minimally so they parse.
6. Lines that over-emphasize a tag anchor word by meta-commenting on it (e.g. "Someone will have to choose. The word is 'choose'."). Reduce to the plain line without the meta-commentary.
7. Basic coherence/formatting fixes only: stray asterisks or markdown in dialogue, dialogue that addresses the wrong addressee mid-line. Do NOT rewrite for style, do NOT add or remove story events, keep each line's length and voice similar.

## Hard constraints
- Segment line budgets are INVARIANT: 4-6 / 2-3 / 2-3 lines per act. Your ops must keep every segment within budget.
- Every speaker id and place id must come from the valid lists above.
- Choice descriptions are the PC's first-person decision text; do not delete them.
- Do not edit act titles, tag ids, choice difficulty, attribute fields, or outcome attribute/delta fields.
- Never DELETE the decision line (ids like a0sD) or pass/fail outcome lines (a0sPl0, a0sFl0). If one of those lines is defective, PATCH its dialogue instead.
- If a line is fine, do not patch it.

{hint_block}## Output contract — return ONLY lines of this form, nothing else
PATCH <line_id> | <speaker_id or -> | <new dialogue or -> | <new stage_directions or -> or EMPTY>
DELETE <line_id>
SPLIT <line_id> | <speaker_id> | <second fragment dialogue> | <stage_directions or ->

- In PATCH, use "-" to keep the old value. To blank stage_directions use "EMPTY".
- SPLIT: the second fragment moves to <line_id>x as a new line right after the original. Use SPLIT (not PATCH) for rule 2; use PATCH with the full corrected single-fragment text if the two fragments belong to the same speaker.
- If nothing needs fixing, output the single word: NONE

## Episode {ep['id']} — "{ep['title']}"
{body}
'''
    return prompt

PATCH_RE = re.compile(r'^(PATCH|DELETE|SPLIT)\s+(\S+)(?:\s*\|\s*(.*))?$')

def parse_diff(text):
    """Return list of ops: (op, lid, speaker, dialogue, stage). Raises on garbage."""
    ops = []
    text = text.strip()
    if text == 'NONE':
        return ops
    # strip code fences if the model added them
    text = re.sub(r'^```\w*\n?|\n?```$', '', text, flags=re.M).strip()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        m = PATCH_RE.match(line)
        if not m:
            raise ValueError(f'unparseable diff line: {line[:80]!r}')
        op, lid, rest = m.group(1), m.group(2), m.group(3)
        speaker = dialogue = stage = None
        if rest is not None:
            parts = [p.strip() for p in rest.split('|')]
            if op == 'PATCH' and len(parts) not in (2, 3):
                raise ValueError(f'PATCH needs 2-3 fields: {line[:80]!r}')
            if op == 'SPLIT' and len(parts) not in (2, 3):
                raise ValueError(f'SPLIT needs 2-3 fields: {line[:80]!r}')
            speaker = parts[0]
            dialogue = parts[1] if len(parts) > 1 else None
            stage = parts[2] if len(parts) > 2 else None
        ops.append((op, lid, speaker, dialogue, stage))
    return ops

def apply_diff(ep, ops, valid_chars, valid_places):
    """Apply ops to a deep copy of ep. Raises ValueError on invalid references.
    All ops refer to ORIGINAL line numbering; per-segment index offsets are
    tracked across SPLIT inserts and DELETEs."""
    ep = json.loads(json.dumps(ep))
    segments = {}   # seg_key -> lines list
    singles = {}    # lid -> line dict (decision + outcomes)
    choices = {}
    for ai, act in enumerate(ep['acts']):
        for si, seg in enumerate(act['segments']):
            if seg['type'] == 'narrative':
                segments[f'a{ai}s{si}'] = seg['lines']
        dec = act['decision']
        singles[f'a{ai}sD'] = dec['line']
        for ci, ch in enumerate(dec['choices']):
            choices[f'a{ai}sCl{ci}'] = ch
            singles[f'a{ai}sPl{ci}'] = ch['pass_outcome']['line']
            singles[f'a{ai}sFl{ci}'] = ch['fail_outcome']['line']

    LID_RE = re.compile(r'^(a\d+s(?:\d|D|C|P|F))(l\d+)?(x?)$')

    def check_line_ref(lid):
        m = LID_RE.match(lid)
        if not m:
            raise ValueError(f'unknown line id: {lid}')
        return m

    def apply_patch(lid, target, op, speaker, dialogue, stage):
        # outcome-line speakers are pipeline-invariant (foreground char delivers
        # outcomes) — never reassign them, only fix their dialogue.
        if op == 'PATCH' and re.match(r'^a\d+s[PF]', lid):
            speaker = None
        if speaker not in (None, '-'):
            if speaker not in valid_chars:
                raise ValueError(f'invalid speaker {speaker} in {lid}')
            target['character'] = speaker
        if dialogue not in (None, '-'):
            target['dialogue'] = dialogue
        if stage == 'EMPTY':
            target['stage_directions'] = ''
        elif stage not in (None, '-'):
            target['stage_directions'] = stage

    # 1) choice descriptions
    for op, lid, speaker, dialogue, stage in ops:
        m = check_line_ref(lid)
        if m.group(1) in choices:
            if op == 'DELETE':
                raise ValueError('cannot DELETE a choice description')
            if op == 'SPLIT':
                raise ValueError('cannot SPLIT a choice description')
            if dialogue not in (None, '-'):
                choices[m.group(1)]['description'] = dialogue

    # 2) single lines (decision + outcomes)
    for op, lid, speaker, dialogue, stage in ops:
        m = check_line_ref(lid)
        if m.group(1) not in segments and m.group(1) in choices:
            continue
        if m.group(1) in segments:
            continue
        if lid not in singles:
            raise ValueError(f'unknown line id: {lid}')
        target = singles[lid]
        if op == 'DELETE':
            raise ValueError(f'cannot delete {lid}')
        apply_patch(lid, target, op, speaker, dialogue, stage)

    # 3) segment lines, grouped per segment, processed in original-index order
    by_seg = {}
    for op, lid, speaker, dialogue, stage in ops:
        m = check_line_ref(lid)
        if m.group(1) in segments:
            by_seg.setdefault(m.group(1), []).append((op, lid, m, speaker, dialogue, stage))
    for seg_key, sop in by_seg.items():
        lines = segments[seg_key]
        for t in sop:
            if not t[2].group(2):
                raise ValueError(f'missing line index: {t[1]}')
        sop.sort(key=lambda t: (int(t[2].group(2)[1:]), t[2].group(3)))
        offset = 0
        for op, lid, m, speaker, dialogue, stage in sop:
            orig = int(m.group(2)[1:])
            idx = orig + offset
            if idx >= len(lines):
                raise ValueError(f'line id out of range after shifts: {lid}')
            target = lines[idx]
            if op == 'DELETE':
                del lines[idx]
                offset -= 1
                continue
            apply_patch(lid, target, op, speaker, dialogue, stage)
            if op == 'SPLIT':
                if not dialogue:
                    raise ValueError(f'SPLIT needs dialogue for {lid}')
                new_line = {'character': speaker if speaker not in (None, '-') else target['character'],
                            'place': target['place'], 'dialogue': dialogue,
                            'stage_directions': '' if stage in (None, '-') else stage}
                if new_line['character'] not in valid_chars:
                    raise ValueError(f'invalid speaker {new_line["character"]}')
                lines.insert(idx + 1, new_line)
                offset += 1
    return ep

def validate_episode(ep, valid_chars, valid_places, valid_attrs, tag_ids):
    errs = []
    if len(ep.get('acts', [])) != 4:
        return ['not 4 acts']
    for ai, act in enumerate(ep['acts']):
        segs = act['segments']
        if len(segs) != 5 or segs[0]['type'] != 'narrative':
            errs.append(f'act{ai}: bad segment layout')
            continue
        budgets = [(0, 4, 6), (2, 2, 3), (4, 2, 3)]
        for si, lo, hi in budgets:
            n = len(segs[si]['lines'])
            if not (lo <= n <= hi):
                errs.append(f'act{ai} seg{si}: {n} lines outside [{lo},{hi}]')
        for si in (1, 3):
            if segs[si]['type'] != 'tag' or segs[si]['tag'] not in tag_ids:
                errs.append(f'act{ai} seg{si}: bad tag')
        for si, lo, hi in budgets:
            for li, ln in enumerate(segs[si]['lines']):
                errs += check_line(ln, f'a{ai}s{si}l{li}', valid_chars, valid_places)
        dec = act['decision']
        errs += check_line(dec['line'], f'a{ai}D', valid_chars, valid_places)
        chs = dec['choices']
        if len(chs) != 3 or [c['difficulty'] for c in chs] != ['easy', 'medium', 'hard']:
            errs.append(f'act{ai}: bad choices')
        for ci, ch in enumerate(chs):
            if ch['attribute'] not in valid_attrs:
                errs.append(f'act{ai} choice{ci}: bad attribute')
            if not ch['description'].strip():
                errs.append(f'act{ai} choice{ci}: empty description')
            for oc in ('pass_outcome', 'fail_outcome'):
                errs += check_line(ch[oc]['line'], f'a{ai}{ci}{oc}', valid_chars, valid_places)
                if ch[oc]['attribute'] not in valid_attrs:
                    errs.append(f'act{ai} choice{ci} {oc}: bad attribute')
    return errs

def check_line(ln, where, valid_chars, valid_places):
    errs = []
    if ln.get('character') not in valid_chars:
        errs.append(f'{where}: invalid character {ln.get("character")}')
    if ln.get('place') not in valid_places:
        errs.append(f'{where}: invalid place {ln.get("place")}')
    d = ln.get('dialogue')
    if not isinstance(d, str) or not d.strip() or d.strip() in ('[None]',):
        errs.append(f'{where}: empty/bad dialogue')
    if THAI_RE.search(d or ''):
        errs.append(f'{where}: Thai unicode in dialogue')
    sd = ln.get('stage_directions')
    if not isinstance(sd, str):
        errs.append(f'{where}: stage_directions not string')
    elif THAI_RE.search(sd):
        errs.append(f'{where}: Thai unicode in stage')
    return errs

def build_hints(ep):
    """Deterministically flagged lines, rendered for the prompt."""
    hints = []
    seen = {}
    for p, ln in iter_line_paths(ep):
        d = (ln.get('dialogue') or '').strip()
        lid = line_id(*p)
        if d:
            seen.setdefault(d, []).append(lid)
        if 'boat nudges its post' in d:
            hints.append(f'- {lid}: repeated stock line "A boat nudges its post and settles." — keep AT MOST ONE occurrence per episode (rewrite or delete the rest, respecting segment budgets).')
        if re.search(r'[Tt]he word (is|was) ["\u2018\u2019\']', d) or re.search(r'[Tt]he word (is|was) ', d):
            hints.append(f'- {lid}: meta-commentary about an anchor word ("{d[:80]}") — remove the meta-commentary, keep only the plain line.')
        if re.search(r'\bof \.\s*$', d) or re.search(r'\bis a \w+ of \.\s*$', d):
            hints.append(f'- {lid}: incomplete sentence ("{d[:80]}") — complete it minimally.')
        sd = (ln.get('stage_directions') or '').strip()
        if sd and len(sd.split()) <= 4 and not re.search(r'\b(he|she|they)\b', sd, re.I) and re.search(r'\b(between|of|without|after|before|space|silence|pause)\b', sd, re.I):
            hints.append(f'- {lid}: stage direction may not be a physical action ("{sd[:60]}") — make it a concrete action or empty it.')
    for d, lids in seen.items():
        if len(lids) > 1:
            hints.append(f'- the exact line "{d[:70]}" appears {len(lids)} times ({", ".join(lids)}) — repeated lines are padding; keep at most one occurrence.')
    return hints

def leftover_flags(ep):
    """Line ids still problematic after a pass: repeated exact lines beyond the
    first occurrence, stock boat lines beyond the first, meta-anchor and
    incomplete-sentence patterns."""
    flags = []
    seen = {}
    for p, ln in iter_line_paths(ep):
        d = (ln.get('dialogue') or '').strip()
        lid = line_id(*p)
        if d:
            seen.setdefault(d, []).append(lid)
        if re.search(r'[Tt]he word (is|was) ', d):
            flags.append((lid, 'anchor-word meta-commentary', d))
        if re.search(r'\bof \.\s*$', d):
            flags.append((lid, 'incomplete sentence', d))
    for d, lids in seen.items():
        if len(lids) > 1:
            for lid in lids[1:]:
                flags.append((lid, 'exact repeated line', d))
    return flags

def build_leftover_prompt(ep, chars, places, flags):
    char_names = {c['id']: c['name'] for c in chars}
    body = render_episode(ep, char_names)
    flag_lines = '\n'.join(f'- {lid}: {why} — "{d[:90]}"' for lid, why, d in flags)
    return f'''You are a meticulous script editor for a narrative RPG. The episode below was already edited; the following numbered lines are STILL defective and must be rewritten in place (PATCH only):

{flag_lines}

Rules:
- Rewrite each flagged line minimally so it fits its immediate scene (same speaker, same act, same tone as surrounding lines). Do not merge lines, do not delete lines, do not add lines.
- For repeated padding lines (e.g. "A boat nudges its post and settles." used as filler), replace each extra occurrence with one concrete, scene-appropriate observation that matches the place and characters present — each replacement must be DIFFERENT from the others.
- Remove any meta-commentary about anchor words (e.g. 'The word was "means."') — keep only the plain story line.
- Complete incomplete sentences minimally.
- Do not touch any other line.
- Output ONLY PATCH lines of the form: PATCH <line_id> | - | <new dialogue> | -

## Episode {ep['id']} — "{ep['title']}"
{body}
'''

def issue_scan(ep):
    """Quick deterministic pre-scan to count targetable issues."""
    found = {'thai': 0, 'markdown': 0, 'boat': 0, 'incomplete': 0, 'meta_anchor': 0}
    for _, ln in iter_line_paths(ep):
        for key in ('dialogue', 'stage_directions'):
            v = ln.get(key) or ''
            if THAI_RE.search(v):
                found['thai'] += 1
            if '*' in v or v.count('"') > 1 or v.count("'") > 2:
                found['markdown'] += 1
            if 'boat nudges its post' in v:
                found['boat'] += 1
            if re.search(r'\bof \.\s*$', v) or re.search(r'\bof\.$', v) or re.search(r'\bis a \w+ of \.', v):
                found['incomplete'] += 1
            if re.search(r"[Tt]he word (is|was) ", v) or re.search(r"anchor word", v):
                found['meta_anchor'] += 1
    return found
