#!/usr/bin/env python3
"""K3 experiment — stage 1: prepare an episode assignment + minimal prompts.

Usage: python3 prepare.py --ep-id ep_010 --foreground char_X --places p1,p2 --tags 12ids
       (all optional; omitted values are drawn at random)
Writes to --out: outline_prompt.md, script_prompt.md (OUTLINE slot left open),
run_config.json.
"""
import argparse, json, os, random, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
import driver  # reuse loaders/helpers from the OR pipeline

def phrases_from_private(text):
    """Pull the 'dialectical noun phrases' bullets from a private plan."""
    m = re.search(r"(?:dialectical\s+)?noun phrases\*?\*?:?\*?\*?\s*\n(.*?)(?=^#{1,4}\s|^\*\*[A-Z]|\Z)", text or "",
                  re.I | re.S | re.M)
    if not m:
        return []
    return [l.strip("- \n") for l in m.group(0).splitlines()
            if l.strip().startswith("-")][:6]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep-id")
    ap.add_argument("--foreground")
    ap.add_argument("--places")
    ap.add_argument("--tags")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)

    chars = driver.load_json(os.path.join(driver.REPO_PUBLIC, "characters.json"))
    places = driver.load_json(os.path.join(driver.REPO_PUBLIC, "places.json"))
    tags = driver.load_json(os.path.join(driver.REPO_PUBLIC, "tags.json"))

    foreground = a.foreground or rng.choice(
        [c["id"] for c in chars if c["id"] not in ("char_narrator", "char_pricha")])
    place_ids = ([p.strip() for p in a.places.split(",")] if a.places
                 else rng.sample([p["id"] for p in places], 2))
    tag_ids = ([t.strip() for t in a.tags.split(",")] if a.tags
               else rng.sample([t["id"] for t in tags], 12))
    ep_id = a.ep_id or "ep_k3_001"

    name_map = driver.build_name_map()
    shared = driver.read_file(os.path.join(driver.WORLD_DIR, "shared_context.md"))
    char_texts = [driver.load_character_text("char_pricha"),
                  driver.load_character_text(foreground)]
    place_texts = [driver.load_place_text(p) for p in place_ids]
    place_texts.append(driver.load_place_text("place_veranda"))
    private_text = driver.load_private_text(foreground)
    place_private = "\n\n".join(
        driver.load_private_text(p) for p in place_ids
        if os.path.exists(os.path.join(driver.PRIVATE_DIR, p + "_private.md")))
    pool = phrases_from_private(private_text) + phrases_from_private(place_private)
    tag_summaries = driver.resolve_tags(tag_ids)
    places_json = places
    allowed = set(place_ids) | {"place_veranda"}
    place_names = "\n".join(f"- {(p.get('name') or '').strip()}"
                            for p in places_json if p["id"] in allowed)
    nicks = driver.nickname_guide(name_map)

    outline_prompt = f"""You are outlining a 4-page script for a Thai-language learning RPG
(canal-side Siam, 1910s-1950s). Output: a 1-page bulleted outline. Nothing else.

# World
{shared}

# Characters
{chr(10).join(char_texts)}

# Places
{chr(10).join(place_texts)}

# Foregrounded character's private plan (secret — plan around it, never state it)
{private_text}

# Dialectical noun phrases on file (use these, don't invent new ones)
{chr(10).join('- ' + p for p in pool)}

# Tags available (pick 8, exactly 2 per act; English themes only — no Thai anywhere)
{tag_summaries}

# The outline must contain
- Act 1 opens on a first beat that includes one of the dialectical noun phrases above AND
  introduces the sticky situation. Act 1 introduces the setting and the characters on stage.
- Act 1 includes a passage where Lek handles or regards several specific objects one by one —
  choose objects whose selection and treatment make his motivation in this story visible.
- Four acts. Each act moves the sticky situation.
- Later acts each include one passage where the foregrounded character handles or regards
  several specific objects one by one — objects chosen so their motivation becomes visible.
- Each act ends with a dilemma FOR LEK, in EXACTLY this machine-parsed format:
  DECISION — <Speaker nickname>: "<the dilemma as a spoken line>" / [easy] <choice text> (attr_<one word>) PASS: "<first-person outcome line>" FAIL: "<first-person outcome line>" / [medium] <choice> (attr_<word>) PASS: "..." FAIL: "..." / [hard] <choice> (attr_<word>) PASS: "..." FAIL: "..."
- For each of the 8 chosen tags: one beat `TAG tag_xxx: <the concrete moment>` plus the single
  English anchor word the script will use to evoke the tag's theme in the line before it.

# Output contract (machine-parsed)
### Act 1
<numbered beats, one event each; characters named by the nicknames below>
...
### Act 4
...
## TAG PLAN
- tag_xxx — English anchor word: "word" — act N — <the beat it attaches to>

# Nicknames (binding)
{nicks}
"""

    script_prompt = f"""You are the scriptwriter for a Thai-language learning RPG
(canal-side Siam, 1910s-1950s). Continue the outlined story as a SCRIPT. Write all four
acts in one pass. Nothing but the script.

# The outline (binding — every beat happens, nothing invented beyond it)
{{{{OUTLINE}}}}

# Dialectical noun phrases (work them in as plain noun phrases; never explain them)
{chr(10).join('- ' + p for p in pool)}

# Tag anchors (binding: the line carrying each [[tag_xxx]] marker must be primed by the
# line before it using that tag's anchor word or its close field; English only)
{{{{ANCHORS}}}}

# Names (binding; nicknames only)
{nicks}

# Places (each act's PLACE: line must copy one of these EXACTLY)
{place_names}

# Format contract (machine-parsed, exact)
## Act N — <short evocative title, different for each act>
PLACE: <exact place name>
Then script lines, each one of:
  NARRATOR: <setting description only — never a character's action, never quoted speech>
  <Nickname>: [physical action in brackets, optional] "<speech, optional>"
A line may end with a [[tag_xxx]] marker.
Each act: 4-6 lines, then a line carrying the first tag, 2-3 lines, a line carrying the
second tag, 2-3 lines — 8-12 lines per act total, exactly 2 tags per act.
Never write the DECISION — end each act on the line that leads into it.
No Thai characters. No "like" or "as if".
"""

    os.makedirs(a.out, exist_ok=True)
    open(os.path.join(a.out, "outline_prompt.md"), "w").write(outline_prompt)
    open(os.path.join(a.out, "script_prompt.md"), "w").write(script_prompt)
    json.dump({"ep_id": ep_id, "foreground": foreground, "places": place_ids,
               "tags12": tag_ids}, open(os.path.join(a.out, "run_config.json"), "w"), indent=1)
    print(f"prepared {ep_id}: fg={foreground} places={place_ids} tags={tag_ids}")
    print(f"prompts + config in {a.out}")

if __name__ == "__main__":
    main()
