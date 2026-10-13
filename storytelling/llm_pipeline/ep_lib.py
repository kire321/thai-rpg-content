"""Shared library for the LLM episode pipeline: prompt building, markdown parsing,
structural validation/fixups. Used by ep_worker.py and assembly scripts."""
import json, re, os, html

REPO = "/mnt/agents/thai-rpg-content"
WORK = "/mnt/agents/work/ep170"
KEY_PATH = "/mnt/agents/.secrets/or_key"
MODEL = "deepseek/deepseek-v4-flash"

ATTR_WORD_HOARD = "attr_word_hoard"

# ---------------------------------------------------------------- data maps

def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def build_alias_maps():
    chars = load_json(f"{REPO}/public/characters.json")
    places = load_json(f"{REPO}/public/places.json")
    cmap = {}
    for c in chars:
        aliases = {c["id"]}
        name = c["name"]
        aliases.add(name)
        aliases.add(re.sub(r"\s*\(.*?\)\s*", "", name))
        for m in re.findall(r"\((.*?)\)", name):
            aliases.add(m)
        # first/last tokens
        toks = re.sub(r"[()']", "", name).split()
        for t in toks:
            if len(t) > 2:
                aliases.add(t)
        for a in aliases:
            cmap[norm(a)] = c["id"]
    # hard aliases observed in model output
    cmap.update({
        "POM": "char_pornchai", "WAN": "char_sangwan", "LEK": "char_pricha",
        "KAMNAN": "char_mor_duang", "KAMNAN NOI": "char_mor_duang",
        "PHRA KAM": "char_phra_kam", "MONK": "char_monk",
        "NARRATOR": "char_narrator", "THE NARRATOR": "char_narrator",
        "FIRE STOKER": "char_fire_stoker", "THE FIRE STOKER": "char_fire_stoker",
        "TAX CLERK": "char_tax_clerk", "THE TAX CLERK": "char_tax_clerk",
        "TYPE MONITOR": "char_type_monitor", "THE TYPE MONITOR": "char_type_monitor",
        "TIMEKEEPER": "char_funeral_timekeeper", "THE TIMEKEEPER": "char_funeral_timekeeper",
        "FUNERAL TIMEKEEPER": "char_funeral_timekeeper",
        "DRUMMER": "char_water_blessing_drummer",
        "GAUGE KEEPER": "char_rain_gauge_keeper", "KEEPER": "char_rain_gauge_keeper",
        "THE KEEPER": "char_rain_gauge_keeper",
        "APPRAISER": "char_pawnshop_appraiser", "THE APPRAISER": "char_pawnshop_appraiser",
        "PAWN SHOP APPRAISER": "char_pawnshop_appraiser",
        "OFFICER": "char_district_officer", "THE DISTRICT OFFICER": "char_district_officer",
        "DISTRICT OFFICER": "char_district_officer",
        "STOKER": "char_fire_stoker", "CLERK": "char_tax_clerk",
        "MONITOR": "char_type_monitor", "THE MONK": "char_monk",
        "MAE": "char_narrator", "MOTHER": "char_narrator",
    })
    pmap = {}
    for p in places:
        pmap[norm(p["name"])] = p["id"]
        pmap[norm(p["id"])] = p["id"]
        pmap[norm(p["id"].replace("place_", ""))] = p["id"]
        toks = p["name"].replace("The ", "").split()
        if toks:
            pmap[norm(" ".join(toks[:2]))] = p["id"]
    pmap.update({"VERANDA": "place_veranda", "SCHOOL VERANDA": "place_veranda",
                 "LANDING": "place_letter_writers_landing"})
    return cmap, pmap

def norm(s):
    s = s.upper()
    s = re.sub(r"[’']", "", s)
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

CHAR_MAP, PLACE_MAP = build_alias_maps()

# ---------------------------------------------------------------- anchors

STOP = set("""I YOU HE SHE IT WE THEY THE A AN AND OR BUT IF THEN THAN THAT THIS THESE
THOSE IS ARE WAS WERE BE BEEN BEING DO DOES DID DONE HAVE HAS HAD HAVING CAN COULD
WILL WOULD SHALL SHOULD MAY MIGHT MUST NOT NO YES TO OF IN ON AT FOR WITH WITHOUT
ABOUT INTO THROUGH DURING BEFORE AFTER ABOVE BELOW FROM UP DOWN OUT OFF OVER UNDER
AGAIN FURTHER ONCE HERE THERE WHEN WHERE WHY HOW ALL ANY BOTH EACH FEW MORE MOST
OTHER SOME SUCH ONLY OWN SAME SO THAN TOO VERY JUST ALSO NOW MY YOUR HIS HER ITS OUR
THEIR WHAT WHICH WHO WHOM AM ME HIM US THEM S DON T RE LL VE DON T DOESN DIDN
ISN AREN WASN WEREN CAN T COULDN SHOULDN WOULDN""".split())

def anchor_for(tag):
    name = tag.get("name", "")
    m = re.match(r"^([a-z][a-z_]*?)(?:_\d+)?$", name)
    if m and not name.startswith("tag"):
        w = m.group(1).replace("_", " ")
        if w and w not in STOP:
            return w
    for th in tag.get("themes", []):
        for w in re.findall(r"[A-Za-z']+", th):
            w = w.lower().strip("'")
            if len(w) > 2 and w not in STOP:
                return w
    return "word"

# ---------------------------------------------------------------- prompt

CRAFT_AND_FORMAT = """### Craft requirements (part of the test)

1. **Making sense first.** The literal layer must parse on its own: who wants what, what blocks it, what changed. A reader who skips every figure of speech must still follow the plot. Confusion is failure, not depth.
2. **Sticky situation.** The episode hangs on a cross-purposes situation between **two characters who are both physically present** in the scenes. It must NOT be a transaction (no externally imposed requirement — no fees, registrations, or filings as the spine of the plot). It must NOT be an argument (no diametrically opposed interests — not "I want it / you want it destroyed"). The model: two people need the **same object** because it **means different things** to each — neither is wrong, and the story argues for neither. Build the cross-purposes around the foregrounded character.
3. **Situation-relevant inventories.** Show each character's motivation through collections they keep and describe with a connoisseur's exact, loving eye — and every inventory must bear on the sticky situation (it demonstrates what its keeper wants *in this conflict*).
4. **Two-sided empathy.** Give the reader a reason to feel for each side of the cross-purposes: one inventory and one ache per side. Neither side may be a strawman.
5. **Distinct personalities.** Every named character must be identifiable from dialogue alone: keep each blueprint's tics, speech markers, and habits consistent. The foregrounded character's personality must be unmistakable by the end.
6. **Dialectical phrases, sparingly.** Use about ONE thesis noun phrase per act, applied directly with no "like" or "as if" — and put ONE of them in the episode's first line. All other narration and dialogue stays literal.
7. **First line.** The opening line must name at least one character implicated in the sticky situation, carry one dialectical phrase, and state the sticky situation itself.
8. **Register and restraint.** No melodrama, no narrator commentary on what scenes mean, no similes imported from outside the story's world. The supernatural stays at the level of custom and rumor, never spectacle.
9. **Language.** Write all story text in English. Do not use Thai script anywhere. Romanized Thai words (e.g., *nam jai*) are welcome.

### Required structure (markdown script)

- `# <Episode title>` then `## Act 1 — <act title>` through `## Act 4 — <act title>`.
- Each act contains, in order: a narrative block of 4-5 screenplay-style lines; a tag line `[TAG: tag_xxx — anchor: "word"]`; a narrative block of 2–3 lines; the second tag line; a narrative block of 2–3 lines; then a DECISION block.
- A narrative line looks like: `NAME (place_id): "Dialogue." *Stage direction.*` Narration with no speaker uses `NARRATOR (place_id): ...`. Keep lines short — this is game text, not prose paragraphs.
- **Anchor rule:** the anchor word of each tag must appear in the LAST dialogue line of the narrative block immediately before that tag.
- The DECISION block looks like:

```
### DECISION — Lek (char_pricha) at <place_id>
**Situation:** "One spoken line from a character that frames the dilemma for Lek."
- **EASY** (checks <attribute>): "Lek's first-person choice, e.g. 'I will ...'"
  - PASS (+1 <attribute>): <foregrounded character name>: "Outcome line."
  - FAIL (+0): <same speaker>: "Outcome line."
- **MEDIUM** (checks <attribute>): "..."
  - PASS (+1 ...): ...
  - FAIL (+0): ...
- **HARD** (bypass — checks attr_word_hoard): "..."
  - PASS (+1 ...): ...
  - FAIL (+0): ...
```

- Every act's EASY/MEDIUM/HARD triple must follow that act's decision pair orientation exactly (specified below). The three options must be genuine dilemmas — each sacrifices something real, none is obviously right, and they must be consistent with the act's fiction.
- The PASS/FAIL outcome lines are spoken by the foregrounded character and show a change in how they regard Lek — warmth, trust, distance, amusement. **Outcomes never change the plot:** whichever option the player picks, the observable story afterwards is identical. Do not write outcomes that assert different facts about the world.
- The episode title and act titles are yours. The four acts should escalate: introduce the situation; tighten it; bring it to a head; transform it so it stops pressing.

Return only the markdown episode. Do not explain your choices. Do not summarize. Do not use tools."""

def build_prompt(package):
    fg = package["foregrounded"]
    p = []
    p.append('You are writing one episode of an educational narrative RPG. The game teaches intermediate Thai vocabulary by embedding quiz "tags" inside a serious literary story set in a canal-side Siamese village in the first half of the twentieth century. Your job is to write the episode. Everything you need is in this message: do not use any tools, do not ask any questions, do not look anything up. Return only the finished episode as a single markdown reply — no commentary, no explanations, no notes about your process.')
    p.append("")
    p.append("### The world (canon — do not contradict)")
    p.append('A canal-side village in Siam, monsoon season. Homes and shops cluster along the water; the social heart of the village is a wooden **veranda** (`place_veranda`) where residents gather in the evening. The player character is **Lek** (`char_pricha`), a young village clerk who helps everyone and belongs to no one. Around him move a fixed cast of recurring villagers (below). The tone is literary realism with a faint shimmer of the supernatural: the village runs on records, letters, ledgers, rites, and debts — and on Thai concepts of heart-water (generosity), deference (kreng jai), and merit poured for the dead.')
    p.append("")
    p.append("### The dealt narrative elements (fixed — use exactly what is dealt)")
    p.append("")
    p.append(f"**Foregrounded character (must appear in every act, and delivers every decision outcome line): {fg['name']}** (`{fg['id']}`)")
    p.append("```")
    p.append(fg["private_plan"].strip())
    p.append("```")
    p.append("")
    p.append("**Supporting cast (use as needed; each has a fixed personality):**")
    for cid in package["cast_priority_order"]:
        if cid == fg["id"]:
            continue
        plan = package["cast_plans"].get(cid, "")
        p.append(f"- `{cid}`:")
        p.append("```")
        p.append(plan.strip())
        p.append("```")
    p.append("")
    p.append("**Places (use in this exact order: act 1 uses the first, act 2 the second, act 3 the third; act 4 returns to the veranda `place_veranda`). Each place comes with one specialist NPC who appears in that act:**")
    for pl in package["places_in_priority_order"]:
        p.append(f"- `{pl['id']}` — {pl.get('name','')}:")
        p.append("```")
        p.append(pl["private_plan"].strip())
        for ex in pl.get("extras", []):
            p.append("")
            p.append(f"NPC {ex['id']} — {ex.get('name','')}:")
            p.append(ex["private_plan"].strip())
        p.append("```")
    p.append("")
    p.append("**Quiz tags (exactly two per act, in this order). Each tag quizzes the vocabulary of its listed theme sentences; the word shown after 'anchor' must appear in dialogue:**")
    for ai, act in enumerate(package["acts"], 1):
        for t in act["tags"]:
            themes = " / ".join(t.get("themes", []))
            p.append(f"- Act {ai}: `{t['id']}` (themes: {themes}) — anchor: **{anchor_for(t)}**")
    p.append("")
    p.append("**Decision attributes (fixed meanings):**")
    p.append("- `attr_heart_water` — *nam jai*, generosity of spirit, giving without being asked.")
    p.append("- `attr_deference` — *kreng jai*, deferential consideration; sparing others discomfort.")
    p.append("- `attr_ledger` — the record: accuracy, account-keeping, what is written down and what it costs.")
    p.append("- `attr_merit_water` — merit-water: the rites and offerings that carry goodness to the dead.")
    p.append("- `attr_word_hoard` — the word-hoard: vocabulary, phrasing, saying the right word at the right time.")
    p.append("")
    p.append("**Decision pairs (one per act; orientation is fixed):**")
    for ai, act in enumerate(package["acts"], 1):
        pr = act["priority_pair"]["priorities"]
        p.append(f"- Act {ai}: priorities `[{pr[0]}, {pr[1]}]` — EASY choice checks `{pr[1]}`; MEDIUM choice checks `{pr[0]}`; HARD bypasses the dilemma (checks `attr_word_hoard`).")
    p.append('Thematically: each EASY option upholds the second value at the first one\'s expense; each MEDIUM upholds the first at the second\'s expense; HARD dodges the value-conflict at a different, concrete price. "Bypasses" never means "for free."')
    p.append("")
    p.append(CRAFT_AND_FORMAT)
    return "\n".join(p)

# ---------------------------------------------------------------- parsing

THAI_RE = re.compile(r"[\u0E00-\u0E7F]+")

def clean_dialogue(s):
    s = THAI_RE.sub("", s)
    s = html.unescape(s)
    s = s.replace("**", "")
    return s.strip()

def parse_line(raw, default_place):
    """Parse 'NAME (place): "Dialogue." *stage*' -> line dict or None."""
    s = raw.strip().lstrip("- ").strip()
    s = re.sub(r"^\*?\*?[A-Z][A-Z .'’\-]*?\*?\*?:\s*", "", s) if False else s
    m = re.match(r"^(?P<who>[A-Z][A-Za-z0-9 .'’\-]*?)\s*(?:\((?P<place>[A-Za-z_ ]+)\))?\s*:\s*(?P<body>.+)$", s)
    if not m:
        return None
    who = m.group("who").strip()
    body = m.group("body").strip().replace("**", "")
    place_raw = (m.group("place") or "").strip()
    # stage directions in *...* or italics
    sd = " ".join(re.findall(r"\*([^*]+)\*", body))
    dlg = re.sub(r"\*[^*]+\*", " ", body)
    dlg = re.sub(r"^\"|\"$", "", dlg.strip())
    dlg = re.sub(r"^\u201c|\u201d$", "", dlg)
    dlg = clean_dialogue(dlg)
    sd = clean_dialogue(sd) if sd else ""
    if not dlg and sd:
        dlg, sd = sd, ""  # stage-direction-only line: promote the direction to dialogue
    if not dlg:
        return None
    cid = CHAR_MAP.get(norm(who))
    if cid is None:
        cid = "char_narrator"
    pid = PLACE_MAP.get(norm(place_raw)) if place_raw else None
    if pid is None:
        pid = default_place
    return {"character": cid, "place": pid, "dialogue": dlg,
            "stage_directions": clean_dialogue(sd) if sd else ""}

def parse_act_block(text, default_place):
    lines = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        if raw.strip().startswith(("[TAG:", "### DECISION", "**Situation:**", "- **", "- PASS", "- FAIL", "  - PASS", "  - FAIL")):
            continue
        ln = parse_line(raw, default_place)
        if ln:
            lines.append(ln)
    return lines

PAD_LINES = [
    "The moment holds, and the village waits.",
    "Somewhere down the canal, a dog barks once and thinks better of it.",
    "The air smells of rain that has not fallen yet.",
    "No one on the landing speaks first.",
    "A boat nudges its post and settles.",
    "The lamplight leans with the breeze.",
]

def pad_block(block, place, target, before_last=False):
    """Pad a thin block with narrator bridging lines up to target size."""
    while len(block) < target:
        ln = {"character": "char_narrator", "place": place,
              "dialogue": PAD_LINES[(len(block) * 3 + len(place)) % len(PAD_LINES)],
              "stage_directions": ""}
        if before_last and block:
            block.insert(len(block) - 1, ln)
        else:
            block.append(ln)
    return block

def enforce_caps(b1, b2, b3, place):
    issues = []
    while len(b1) > 6:
        b1.pop(1); issues.append("trimmed-b1")
    while len(b1) < 4 and len(b2) > 2:
        b1.append(b2.pop(0)); issues.append("moved-b2-to-b1")
    if len(b1) < 4:
        pad_block(b1, place, 4, before_last=True); issues.append("padded-b1")
    while len(b2) > 3:
        b2.pop(1); issues.append("trimmed-b2")
    while len(b2) < 2 and len(b3) > 2:
        b2.append(b3.pop(0)); issues.append("moved-b3-to-b2")
    if len(b2) < 2:
        pad_block(b2, place, 2); issues.append("padded-b2")
    while len(b3) > 3:
        b3.pop(1); issues.append("trimmed-b3")
    if len(b3) < 2:
        pad_block(b3, place, 2); issues.append("padded-b3")
    return issues

def word_in(anchor, text):
    return re.search(r"\b" + re.escape(anchor) + r"\b", text, re.I) is not None

def fix_anchor(block, anchor):
    """Ensure anchor appears in last dialogue line; returns True if patched."""
    if not block:
        return False
    if word_in(anchor, block[-1]["dialogue"]):
        return False
    for i, ln in enumerate(block[:-1]):
        if word_in(anchor, ln["dialogue"]):
            block.append(block.pop(i))  # move matched line to the end
            return True
    block[-1]["dialogue"] = (block[-1]["dialogue"].rstrip(".!?") +
                             f'. The word was "{anchor}."').strip()
    return True

def parse_decision(text, fg_id, default_place, pair):
    """Parse the DECISION block. Returns decision dict or None."""
    text = text.replace("**", "")  # bold markers are formatting noise here
    sit = re.search(r"\*\*Situation:\*\*\s*(?:[A-Za-z][A-Za-z0-9 .'’\-]*?\s+to\s+Lek\s*:\s*)?[\"“](.+?)[\"”]\s*$", text, re.M)
    situation = clean_dialogue(sit.group(1)) if sit else "The choice is yours, Lek."
    choices = []
    # choice headers: tolerate missing bullets, missing colons, nested/absent parens.
    # stage 1: difficulty keyword; stage 2: junk up to first quote (attribute hunted in junk);
    # stage 3: rest of line is the description.
    hdr = list(re.finditer(r'^\s*(?:-\s*)?(?:\*\*)?(EASY|MEDIUM|HARD)\b(.*?)[\"“](.*)$', text, re.M))
    for i, m in enumerate(hdr):
        diff = m.group(1).lower()
        am = re.search(r"attr_\w+", m.group(2))
        attr = am.group(0) if am else ATTR_WORD_HOARD
        desc = m.group(3).strip()
        if desc.endswith(('"', '\u201d')):
            desc = desc[:-1]
        end = hdr[i + 1].start() if i + 1 < len(hdr) else len(text)
        chunk = text[m.end():end]
        def outcome(kind, delta):
            om = re.search(kind + r"\s*\(\+(\d)\s*([\w\-]+)?\)\s*:\s*(?:([A-Z][A-Za-z0-9 .'’\-]*?)\s*:\s*)?[\"“](.*?)[\"”]", chunk)
            if not om:
                return {"line": {"character": fg_id, "place": default_place,
                                 "dialogue": "It is done.", "stage_directions": ""},
                        "attribute": ATTR_WORD_HOARD, "delta": delta}
            dlg = clean_dialogue(om.group(4))
            return {"line": {"character": fg_id, "place": default_place,
                             "dialogue": dlg, "stage_directions": ""},
                    "attribute": (om.group(2) or ATTR_WORD_HOARD), "delta": delta}
        choices.append({
            "description": clean_dialogue(desc),
            "difficulty": diff,
            "attribute": attr,
            "pass_outcome": outcome("PASS", 1),
            "fail_outcome": outcome("FAIL", 0),
        })
    if len(choices) != 3:
        return None
    # enforce orientation
    a, b = pair["priorities"]
    enforced = {"easy": b, "medium": a, "hard": ATTR_WORD_HOARD}
    for ch in choices:
        want = enforced[ch["difficulty"]]
        if ch["attribute"] != want:
            ch["attribute"] = want
        ch["pass_outcome"]["attribute"] = want
        ch["fail_outcome"]["attribute"] = want
    return {"line": {"character": fg_id, "place": default_place,
                     "dialogue": situation, "stage_directions": ""},
            "choices": choices}

def parse_episode(md, package):
    """Parse model markdown into CMS episode JSON. Returns (episode, issues)."""
    issues = []
    title_m = re.search(r"^#\s+(.+)$", md, re.M)
    title = clean_dialogue(title_m.group(1)) if title_m else package["episode_id"]
    # split acts
    acts_raw = []
    for m in re.finditer(r"^##\s+(?!#)(Act\s+\d[^\n]*)$", md, re.M):
        acts_raw.append((m.group(1), m.start()))
    if len(acts_raw) < 4:
        return None, ["acts-found-%d" % len(acts_raw)]
    fg_id = package["foregrounded"]["id"]
    places = [pl["id"] for pl in package["places_in_priority_order"]]
    while len(places) < 4:
        places.append("place_veranda")
    places[3] = "place_veranda"
    tag_ids = [t["id"] for act in package["acts"] for t in act["tags"]]
    anchors = [anchor_for(t) for act in package["acts"] for t in act["tags"]]
    acts = []
    for ai in range(4):
        header, start = acts_raw[ai]
        end = acts_raw[ai + 1][1] if ai + 1 < len(acts_raw) else len(md)
        body = md[start:end]
        act_title = clean_dialogue(header.split("—", 1)[-1].strip()) if "—" in header else clean_dialogue(header)
        place = places[ai]
        # find the two tag markers and decision
        tag_marks = list(re.finditer(r"\[TAG:\s*(tag_\d+)", body))
        dec_m = re.search(r"^###\s*DECISION", body, re.M)
        if len(tag_marks) < 2 or not dec_m:
            return None, [f"act{ai+1}-markers-missing"]
        b1_text = body[:tag_marks[0].start()]
        b2_text = body[tag_marks[0].end():tag_marks[1].start()]
        b3_text = body[tag_marks[1].end():dec_m.start()]
        dec_text = body[dec_m.start():]
        b1 = parse_act_block(b1_text, place)
        b2 = parse_act_block(b2_text, place)
        b3 = parse_act_block(b3_text, place)
        issues += enforce_caps(b1, b2, b3, place)
        # anchors AFTER all block moves; padding for b1 inserts before its last line
        if fix_anchor(b1, anchors[2 * ai]):
            issues.append(f"act{ai+1}-anchor1-patched")
        if fix_anchor(b2, anchors[2 * ai + 1]):
            issues.append(f"act{ai+1}-anchor2-patched")
        if not (4 <= len(b1) <= 6 and 2 <= len(b2) <= 3 and 2 <= len(b3) <= 3):
            issues.append(f"act{ai+1}-blocksize")
        decision = parse_decision(dec_text, fg_id, place, package["acts"][ai]["priority_pair"])
        if decision is None:
            return None, [f"act{ai+1}-decision-unparsed"]
        acts.append({
            "id": f"act_{ai+1:03d}",
            "title": act_title or f"Act {ai+1}",
            "segments": [
                {"type": "narrative", "lines": b1},
                {"type": "tag", "tag": tag_ids[2 * ai]},
                {"type": "narrative", "lines": b2},
                {"type": "tag", "tag": tag_ids[2 * ai + 1]},
                {"type": "narrative", "lines": b3},
            ],
            "decision": decision,
        })
    return {"id": package["episode_id"], "title": title, "acts": acts}, issues
