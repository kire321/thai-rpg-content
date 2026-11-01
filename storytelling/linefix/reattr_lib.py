#!/usr/bin/env python3
"""Detection of likely misattributed lines + prompt for speaker reassignment."""
import json, re, sys

sys.path.insert(0, '/mnt/agents/work/epfix')
from epfix_lib import iter_line_paths, render_episode, line_id

FP = re.compile(r'\b(I|me|my|mine|myself|we|us|our|ours)\b')
SP = re.compile(r'\b(you|your|yours|yourself)\b', re.I)
QUOTED = re.compile(r'["\u201c\u201d]')
MENTION = re.compile(r'\b(Bua|widow|Widow|Nim)\b')

def detect(ep):
    """Return list of (lid, why, dialogue) for suspicious lines + whether the
    episode mentions Bua/widow/Nim (context flag)."""
    flags = []
    blob = json.dumps(ep)
    mentioned = bool(MENTION.search(blob))
    for p, ln in iter_line_paths(ep):
        if 'character' not in ln:
            continue
        if ln['character'] != 'char_narrator':
            continue
        d = ln.get('dialogue') or ''
        why = []
        if FP.search(d):
            why.append('first-person pronoun in narrator line')
        if SP.search(d):
            why.append('second-person pronoun in narrator line')
        if (ln.get('stage_directions') or '').strip():
            why.append('narrator line carries a stage direction')
        if QUOTED.search(d):
            why.append('quoted speech inside narrator line')
        if d.strip().endswith('?'):
            why.append('narrator line asks a question')
        if why:
            flags.append((line_id(*p), '; '.join(why), d))
    return flags, mentioned

def build_reattr_prompt(ep, chars, places, flags, mentioned):
    char_names = {c['id']: c['name'] for c in chars}
    cast = '\n'.join(f"- {c['id']} ({c['name']}, type={c['type']}): {c.get('description','')[:160]}"
                     for c in chars)
    place_ids = ', '.join(sorted(p['id'] for p in places))
    flag_block = '\n'.join(f'- {lid}: {why}. Line: "{d[:110]}"' for lid, why, d in flags)
    ctx = ('NOTE: this episode mentions Bua, a widow, or Nim — lines fitting an elderly bereaved '
           'widow (Nim\'s mother archetype) should go to char_old_lady.'
           if mentioned else '')
    body = render_episode(ep, char_names)
    return f'''You are fixing speaker attribution in one episode of a narrative RPG rendered as numbered lines.

## Valid speakers (use these exact ids)
{cast}

## Valid place ids
{place_ids}

## Suspicious lines flagged by automated checks
{flag_block}
{ctx}
## Attribution rules
- Flagged status is a HEURISTIC, not proof. Many flagged lines are legitimate scene description.
- PURE SCENE DESCRIPTION always stays with char_narrator, even if flagged: evening light, who is
  present, objects, weather, ambient sounds, summary sentences like "The moment holds, and the village
  waits." Do NOT reassign these.
- Reassign a narrator line ONLY if it carries a clear VOICE: a first-person claim ("I", "my"),
  a direct address to a person present ("you" aimed at a character), quoted speech, an imperative or
  question directed at someone, or a personal opinion about what should be done.
- char_narrator never carries stage directions — but a stage direction on a description line is a
  parser artifact, NOT evidence of speech. Use the voice test above.
- When reassigning, pick the speaker from context: who speaks the lines immediately before/after, who
  belongs to the place, whom the line addresses. char_old_lady is the elderly widow / Nim's mother
  archetype: dead daughter, mourning, herbal remedies, elder wisdom — when no more specific NPC fits.
- Also reassign any OTHER line (not flagged) whose speaker is clearly wrong, subject to the same
  voice test (e.g. a party member voicing the Old Lady's grief). Never reassign pure description.
- Never change dialogue text or stage directions in this pass — speaker ids only. Never reassign
  pass/fail outcome lines (ids like a0sPl0/a0sFl0) — their speakers are structurally fixed.
- If in doubt, leave the line unchanged. A missed fix is acceptable; a wrong speaker is not.

## Output contract — return ONLY lines of this form, nothing else
PATCH <line_id> | <speaker_id> | - | -
or the single word: NONE

## Episode {ep['id']} — "{ep['title']}"
{body}
'''
