#!/usr/bin/env python3
"""Generate the 170-episode V2 staging expansion.

OpenRouter is the primary generator.  The deterministic writer is an explicit
fallback for offline CI/content review, so a missing key never leaves a partial
or malformed episodes.json.  Both paths produce the same ordered-segment
schema and are validated before each episode is saved.

Usage:
  OPENROUTER_API_KEY=... python generate_episodes_v3.py
  python generate_episodes_v3.py --offline
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
EPISODES_PATH = PUBLIC / "episodes.json"
TAGS_PATH = PUBLIC / "tags.json"
VOCAB_PATH = PUBLIC / "vocab_items.json"
CHARACTERS_PATH = PUBLIC / "characters.json"
PLACES_PATH = PUBLIC / "places.json"
SUBPLOTS_PATH = PUBLIC / "subplots.json"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324"
FALLBACK_MODEL = "deepseek/deepseek-chat"
REFERER = "https://github.com/kire321/thai-rpg-content"

NEW_CHARACTER_IDS = {
    "char_kanya",
    "char_wichai",
    "char_maliwan",
    "char_jintana",
    "char_sakchai",
    "char_pailin",
    "char_rung",
    "char_nop",
    "char_chaiyo",
    "char_lalida",
}
NEW_PLACE_IDS = {
    "place_moonwell_platform",
    "place_iron_kite_docks",
    "place_singing_rice_terraces",
    "place_undertone_bazaar",
    "place_lattice_fisheries",
    "place_bellflower_observatory",
    "place_broken_tether_field",
    "place_echo_cistern",
    "place_cloudstep_village",
    "place_resonant_greenhouse",
}
PARTY_IDS = ["char_chanida", "char_pichit", "char_malee", "char_arthit"]
SUBPLOT_IDS = [
    "subplot_frequency_map",
    "subplot_haunted_ship",
    "subplot_crystal_leg",
    "subplot_listener_warning",
    "subplot_groundless",
]

# Distinct voices keep the offline path readable and also give the OpenRouter
# prompt concrete few-shot guidance without sending the whole 340-episode file.
PARTY_VOICES = {
    "char_chanida": [
        "I can hear the hidden interval; let me answer it before the lattice hardens.",
        "The Orders call this noise, but the pattern is too deliberate to ignore.",
        "Give me one clear breath and I can open a route through that chord.",
    ],
    "char_pichit": [
        "A warning is still a warning when the listener dislikes its meaning.",
        "The quiet between tones matters as much as the note we choose.",
        "We should hear the lattice without pretending it has promised us safety.",
    ],
    "char_malee": [
        "That platform is failing at the joint; I can brace it before we sing again.",
        "Surface crews learn the cost of a beautiful shortcut very quickly.",
        "Hand me the spare coil and keep your feet away from the bright seam.",
    ],
    "char_arthit": [
        "I know this current. It bends toward the wreck route I swore never to use.",
        "Keep the engine low; a safe channel is no good if it announces us.",
        "My old maps end here, so every mark we make must serve the next crew.",
    ],
}

OLD_NPC_HOOKS = {
    "char_villager": "keeps glancing toward the tether that holds their home aloft",
    "char_bandit": "checks the escape skiff and pretends not to be afraid",
    "char_merchant": "counts sealed cargo while listening for a profitable answer",
    "char_monk": "presses two fingers to the crystal and records its pulse",
    "char_scavenger": "tests a salvaged brace against the shifting surface",
    "char_ratana": "reads the object's history through a careful touch",
    "char_kamon": "rests a gauntleted hand on the wall to absorb the surge",
    "char_bussaba": "protects a crystal bloom from the changing air",
    "char_thanet": "tilts his head toward a route no instrument can see",
    "char_suda": "holds her city's core fragment as if it were still alive",
    "char_prayut": "hides a compact tether breaker beneath a work cloth",
    "char_duangjai": "layers a quiet harmony beneath the surrounding noise",
    "char_somsak": "checks three exits before offering a price",
    "char_niran": "stands inside the silence and watches everyone breathe",
    "char_ampa": "unrolls a map whose lines shift when the lattice sings",
}
NEW_NPC_HOOKS = {
    "char_kanya": "checks the anchor weights and listens for a failing tether",
    "char_wichai": "clips a dive bell to his belt and studies the channel below",
    "char_maliwan": "sorts resonance remedies into labeled glass tubes",
    "char_jintana": "keeps a copied permit hidden beneath her route ledger",
    "char_sakchai": "reads the storm from the vibration of the nearest rail",
    "char_pailin": "holds a crystal bowl up until it catches the spoken tone",
    "char_rung": "measures a shelter frame against the next surface tremor",
    "char_nop": "repairs a route tablet with three patient taps",
    "char_chaiyo": "releases a glass kite and follows its answering note",
    "char_lalida": "parks a tuned cable cart and checks the letters in her satchel",
}

ACT_PHASES = [
    ("The First Signal", "a clue surfaces"),
    ("The Narrowing Channel", "the pressure increases"),
    ("The Broken Chord", "the hidden cost becomes clear"),
    ("The Shared Route", "the party chooses what to carry forward"),
]
CHOICE_ACTIONS = [
    ("Trace the frequency map through", "subplot_frequency_map"),
    ("Follow the remembered ship tone beyond", "subplot_haunted_ship"),
    ("Tune Malee's crystal leg against", "subplot_crystal_leg"),
    ("Decode the warning beneath", "subplot_listener_warning"),
    ("Secure a surface shelter beside", "subplot_groundless"),
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


characters = load(CHARACTERS_PATH)
places = load(PLACES_PATH)
tags = load(TAGS_PATH)
vocab_items = load(VOCAB_PATH)
subplots = load(SUBPLOTS_PATH)

CHAR_BY_ID = {item["id"]: item for item in characters}
PLACE_BY_ID = {item["id"]: item for item in places}
TAG_BY_ID = {item["id"]: item for item in tags}
VOCAB_BY_ID = {item["id"]: item for item in vocab_items}
SUBPLOT_BY_ID = {item["id"]: item for item in subplots}
VALID_CHAR_IDS = set(CHAR_BY_ID)
VALID_PLACE_IDS = set(PLACE_BY_ID)
VALID_TAG_IDS = set(TAG_BY_ID)
VALID_SUBPLOT_IDS = set(SUBPLOT_BY_ID)
CHAR_NAME_TO_ID = {}
for item in characters:
    CHAR_NAME_TO_ID[item["name"].lower()] = item["id"]
    CHAR_NAME_TO_ID[item["name"].split()[0].lower()] = item["id"]
PLACE_NAME_TO_ID = {item["name"].lower(): item["id"] for item in places}

OLD_NPCS = [item["id"] for item in characters if item.get("type") == "npc" and item["id"] not in NEW_CHARACTER_IDS]
NEW_NPCS = [item["id"] for item in characters if item["id"] in NEW_CHARACTER_IDS]
OLD_PLACES = [item["id"] for item in places if item["id"] not in NEW_PLACE_IDS]
NEW_PLACES = [item["id"] for item in places if item["id"] in NEW_PLACE_IDS]


def stable_int(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")


def get_tag_usage(episodes: list[dict]) -> dict[str, int]:
    usage = {tag_id: 0 for tag_id in VALID_TAG_IDS}
    for episode in episodes:
        for act in episode.get("acts", []):
            if act.get("tag") in usage:
                usage[act["tag"]] += 1
            for segment in act.get("segments", act.get("steps", [])):
                if isinstance(segment, dict) and segment.get("type") == "tag" and segment.get("tag") in usage:
                    usage[segment["tag"]] += 1
    return usage


def tag_tokens(tag: dict) -> set[str]:
    name = re.sub(r"_\d+$", "", tag.get("name", "").lower())
    return {token for token in re.split(r"[^a-z]+", name) if token}


def tag_similarity(left: dict, right: dict) -> float:
    left_vocab = set(left.get("vocab_item_ids", []))
    right_vocab = set(right.get("vocab_item_ids", []))
    overlap = len(left_vocab & right_vocab) / max(1, len(left_vocab | right_vocab))
    name_overlap = len(tag_tokens(left) & tag_tokens(right))
    return overlap * 5 + name_overlap * 3


def pair_tags(pool: list[str], rng) -> list[tuple[str, str]]:
    """Pair the eight least-used tags so each quiz pair shares a story beat."""
    remaining = [TAG_BY_ID[tag_id] for tag_id in pool]
    pairs: list[tuple[str, str]] = []
    while remaining:
        left = remaining.pop(0)
        best_index = max(
            range(len(remaining)),
            key=lambda index: (
                tag_similarity(left, remaining[index]),
                -stable_int(f"{left['id']}:{remaining[index]['id']}:{rng.random()}"),
            ),
        )
        right = remaining.pop(best_index)
        pair = (left["id"], right["id"])
        pairs.append(pair if rng.random() > 0.5 else (pair[1], pair[0]))
    rng.shuffle(pairs)
    return pairs


def choose_tag_pairs(usage: dict[str, int], rng) -> list[tuple[str, str]]:
    # Sorting by a stable per-run tie-breaker prevents alphabetical clumps while
    # still making the least-used-first distribution deterministic for a seed.
    ranked = sorted(usage, key=lambda tag_id: (usage[tag_id], stable_int(f"{rng.random()}:{tag_id}")))
    pool = ranked[:8]
    return pair_tags(pool, rng)


def clean_vocab_phrase(raw: str, fallback: str) -> str:
    """Turn a textbook gloss into a short, speakable English phrase."""
    phrase = (raw or "").split("/")[0].strip()

    def parenthetical(match: re.Match[str]) -> str:
        content = match.group(1).strip()
        return "" if content in {"…", "...", ""} else content

    phrase = re.sub(r"\(([^)]*)\)", parenthetical, phrase)
    phrase = phrase.replace("…", "").replace("...", "")
    phrase = re.sub(r"\s+", " ", phrase).strip(" ;:")
    if phrase.startswith("'m "):
        phrase = "I am " + phrase[3:]
    elif phrase.startswith("'re "):
        phrase = "We are " + phrase[4:]
    elif phrase.startswith("'s "):
        phrase = "It is " + phrase[3:]
    if len(phrase) < 3:
        phrase = fallback.replace("_", " ")
    return phrase[0].upper() + phrase[1:] if phrase else fallback


def spoken_phrase(context: dict[str, str], variant: int) -> str:
    phrase = context["phrase"] if variant % 2 == 0 else clean_vocab_phrase(context["english"], context["concept"])
    phrase = phrase.strip()
    if phrase and phrase[-1] not in ".!?":
        phrase += "."
    return phrase


def tag_context(tag_id: str, variant: int = 0) -> dict[str, str]:
    tag = TAG_BY_ID[tag_id]
    refs = tag.get("vocab_item_ids", [])
    vocab = VOCAB_BY_ID.get(refs[variant % len(refs)]) if refs else None
    concept = re.sub(r"(?:_\d+)+$", "", tag.get("name", "")).replace("_", " ")
    if concept == "tag" or concept.startswith("tag ") or not re.search(r"[a-zA-Z]", concept):
        concept = "resonance"
    phrase = clean_vocab_phrase(vocab.get("english", "") if vocab else "", concept)
    return {
        "id": tag_id,
        "name": tag.get("name", tag_id),
        "concept": concept,
        "phrase": phrase,
        "thai": vocab.get("thai", "") if vocab else "",
        "english": vocab.get("english", "") if vocab else phrase,
    }


def short_place(place_id: str) -> str:
    name = PLACE_BY_ID[place_id]["name"]
    return name[4:] if name.startswith("The ") else name


def hook_for(char_id: str) -> str:
    return (NEW_NPC_HOOKS | OLD_NPC_HOOKS).get(char_id, "waits for the next change in the surrounding tone")


def line(character: str, place: str, dialogue: str, stage: str = "") -> dict:
    # Keep line objects deliberately closed: LLM alternate fields never leak
    # into the JSON consumed by the CMS.
    return {
        "character": character if character in VALID_CHAR_IDS else "char_narrator",
        "place": place if place in VALID_PLACE_IDS else OLD_PLACES[0],
        "dialogue": dialogue.strip(),
        "stage_directions": str(stage or "").strip(),
    }


def party_voice(char_id: str, rng) -> str:
    return rng.choice(PARTY_VOICES.get(char_id, PARTY_VOICES["char_chanida"]))


def phrase_for(context: dict[str, str], variant: int) -> str:
    return spoken_phrase(context, variant)


def make_narrative_segments(
    *,
    episode_number: int,
    act_index: int,
    pair: tuple[str, str],
    lead_id: str,
    featured_npc_id: str,
    support_npc_id: str,
    primary_place_id: str,
    secondary_place_id: str,
    subplot_id: str,
    rng,
) -> tuple[list[dict], str]:
    first = tag_context(pair[0], (episode_number + act_index) % 5)
    second = tag_context(pair[1], (episode_number + act_index + 1) % 5)
    lead_name = CHAR_BY_ID[lead_id]["name"]
    npc_name = CHAR_BY_ID[featured_npc_id]["name"]
    support_name = CHAR_BY_ID[support_npc_id]["name"]
    primary = short_place(primary_place_id)
    secondary = short_place(secondary_place_id)
    phase, consequence = ACT_PHASES[act_index]
    subplot_name = SUBPLOT_BY_ID[subplot_id]["name"]
    subplot_label = subplot_name[4:] if subplot_name.startswith("The ") else subplot_name
    first_phrase = phrase_for(first, episode_number + act_index)
    second_phrase = phrase_for(second, episode_number + act_index + 1)

    opening_templates = [
        f"At {primary}, a fresh resonance clue reaches the party through the rigging.",
        f"The approach to {primary} begins with a pulse that repeats beneath the engine noise.",
        f"By the time the party reaches {primary}, the lattice has made the first signal impossible to ignore.",
        f"The soundscape of {primary} changes as the party arrives, turning a quiet question into a physical tremor.",
    ]
    middle_templates = [
        f"The clue points toward {secondary}, where a second cadence is hidden beneath the returning echo.",
        f"A pressure wave folds the route toward {secondary}; the next answer depends on listening carefully.",
        f"From {primary} the party can see {secondary} and its distant tone answers the first clue.",
        f"The trail crosses into {secondary}, whose acoustic character makes every spoken phrase carry farther than expected.",
    ]
    closing_templates = [
        f"The immediate consequence is clear: {consequence} around {primary}, while the {subplot_label.lower()} thread gains a dangerous lead.",
        f"The two tones align for one breath, exposing a route between {primary} and {secondary} before the lattice shifts again.",
        f"No one can keep both signals stable for long; the party must decide what the {subplot_label.lower()} clue is worth.",
        f"The echo leaves a precise mark on the map, but it also wakes something beneath {secondary}.",
    ]

    # Four lines before each checkpoint, four between checkpoints, and four
    # after the second checkpoint keeps the new episodes close to the old
    # episodes' average narrative length.
    first_lines = [
        line("char_narrator", primary_place_id, rng.choice(opening_templates), f"The air around {primary} vibrates in a slow interval."),
        line(featured_npc_id, primary_place_id, f"{CHAR_BY_ID[featured_npc_id]['name']} {hook_for(featured_npc_id)}.", f"{npc_name} raises a hand for silence."),
        line(lead_id, primary_place_id, f'"{first_phrase}" {lead_name} says, and the nearest crystal answers the phrase.', "The first resonance ring brightens."),
        line(support_npc_id, primary_place_id, f"{support_name} recognizes the first phrase and points toward the maintenance rail.", f"{support_name} marks one beat on a slate."),
    ]
    second_lines = [
        line("char_narrator", secondary_place_id, rng.choice(middle_templates), f"A low tone travels from {secondary} toward the party."),
        line(featured_npc_id, secondary_place_id, f'"{second_phrase}" {npc_name} replies; the words fit the returning signal exactly.', f"{npc_name} tests the echo with a knuckle."),
        line(lead_id, secondary_place_id, f"{lead_name} connects the two phrases: {party_voice(lead_id, rng)}", "The route narrows to a single luminous seam."),
        line(support_npc_id, secondary_place_id, f"{support_name} reports that the seam leads back toward {primary}, but its timing has changed.", f"The surrounding crystal gives one sharp reply."),
    ]
    third_lines = [
        line("char_narrator", primary_place_id, rng.choice(closing_templates), "Dust lifts from the floor in concentric rings."),
        line(lead_id, primary_place_id, f"{party_voice(lead_id, rng)} The two phrases are parts of one route.", f"{lead_name} keeps the cadence steady."),
        line(featured_npc_id, primary_place_id, f"{npc_name} offers one concrete lead: the next safe interval begins beyond {secondary}.", f"{npc_name} looks toward the open sky."),
        line("char_narrator", primary_place_id, "The lattice settles just long enough to place the choice in the party's hands.", "The next pulse is already forming below."),
    ]
    segments = [
        {"type": "narrative", "lines": first_lines},
        {"type": "tag", "tag": pair[0]},
        {"type": "narrative", "lines": second_lines},
        {"type": "tag", "tag": pair[1]},
        {"type": "narrative", "lines": third_lines},
    ]
    title = f"{phase} at {primary}"
    return segments, title


def make_decision(
    *,
    episode_number: int,
    act_index: int,
    pair: tuple[str, str],
    lead_id: str,
    featured_npc_id: str,
    primary_place_id: str,
    secondary_place_id: str,
    rng,
) -> dict:
    lead_name = CHAR_BY_ID[lead_id]["name"]
    npc_name = CHAR_BY_ID[featured_npc_id]["name"]
    primary = short_place(primary_place_id)
    secondary = short_place(secondary_place_id)
    first = tag_context(pair[0], episode_number + act_index)
    second = tag_context(pair[1], episode_number + act_index + 1)
    # Rotate the subplot window so all five recurring threads receive choices.
    subplot_order = [SUBPLOT_IDS[(episode_number + act_index + offset) % len(SUBPLOT_IDS)] for offset in range(3)]
    choices = []
    difficulties = ["easy", "medium", "hard"]
    actions = [
        f"Ask {npc_name} to identify the first phrase's mark beside {primary}",
        f"Tune the route from {primary} toward {secondary} using the second phrase's cadence",
        f"Cross the unstable seam and recover the clue before {npc_name} loses the signal",
    ]
    for index, (description, difficulty, subplot_id) in enumerate(zip(actions, difficulties, subplot_order)):
        subplot_label = SUBPLOT_BY_ID[subplot_id]["name"]
        subplot_label = subplot_label[4:] if subplot_label.startswith("The ") else subplot_label
        pass_text = [
            f"I held the first phrase long enough to connect {primary} and {secondary}; the route is open.",
            f"I found the second interval inside the noise. {npc_name} can move before the next surge.",
            f"I took the risk and returned with a clean mark for {subplot_label.lower()}.",
        ][index]
        fail_text = [
            "I rushed the first phrase, and the safe channel folded before we could record it.",
            f"I lost the second interval; the clue is still below {primary}, out of reach for now.",
            f"I misread the seam. {npc_name} is safe, but the route has carried our warning toward the wrong skycity.",
        ][index]
        choices.append({
            "description": description,
            "difficulty": difficulty,
            "subplot": subplot_id,
            "pass_outcome": {
                "line": line(lead_id, primary_place_id, pass_text, "The lattice answers with a stable chord."),
                "subplot": subplot_id,
                "delta": 2 if index == 1 else 1,
            },
            "fail_outcome": {
                "line": line(lead_id, primary_place_id, fail_text, "A thin crack of light closes beneath the platform."),
                "subplot": subplot_id,
                "delta": -1 if index == 0 else 0,
            },
        })
    return {
        "line": line(
            lead_id,
            primary_place_id,
            f"The two vocabulary tones are aligned. Which option keeps {npc_name} safe?",
            f"{lead_name} watches the route between {primary} and {secondary}.",
        ),
        "choices": choices,
    }


def _new_place_slots(offset: int) -> list[int]:
    # 227 of 680 primary slots are new (the catalog is 10/30), while every
    # episode still contains at least one new place.
    count = 2 if offset % 3 == 0 else 1
    start = offset % 4
    return [(start + step) % 4 for step in range(count)]


def _new_npc_slots(offset: int) -> list[int]:
    # 272 of 680 featured-NPC slots are new (the catalog is 10/25), while each
    # episode contains at least one old and one new NPC.
    count = 1 if offset % 5 < 2 else 2
    start = (offset * 3) % 4
    return [(start + step) % 4 for step in range(count)]


def _count_before(offset: int, counter) -> int:
    return sum(len(counter(previous)) for previous in range(offset))


def _rank_in_slots(slots: list[int], act_index: int) -> int:
    return slots.index(act_index)


def plan_entities(episode_number: int, act_index: int) -> tuple[str, str, str, str, str]:
    """Return a balanced lead/NPC/place plan for one act."""
    offset = max(0, episode_number - 341)
    all_places = OLD_PLACES + NEW_PLACES
    place_new_slots = _new_place_slots(offset)
    if act_index in place_new_slots:
        new_before = _count_before(offset, _new_place_slots)
        new_index = new_before + _rank_in_slots(place_new_slots, act_index)
        primary = NEW_PLACES[new_index % len(NEW_PLACES)]
    else:
        old_before = _count_before(offset, lambda value: [slot for slot in range(4) if slot not in _new_place_slots(value)])
        old_slots = [slot for slot in range(4) if slot not in place_new_slots]
        old_index = old_before + _rank_in_slots(old_slots, act_index)
        primary = OLD_PLACES[old_index % len(OLD_PLACES)]

    # A second setting is drawn from one global cycle, which keeps the weighted
    # narrative/decision references even across all thirty places.
    secondary_index = (offset * 4 + act_index + 11) % len(all_places)
    secondary = all_places[secondary_index]
    if secondary == primary:
        secondary = all_places[(secondary_index + 1) % len(all_places)]

    npc_new_slots = _new_npc_slots(offset)
    if act_index in npc_new_slots:
        new_before = _count_before(offset, _new_npc_slots)
        new_index = new_before + _rank_in_slots(npc_new_slots, act_index)
        featured = NEW_NPCS[new_index % len(NEW_NPCS)]
        support = OLD_NPCS[(offset * 4 + act_index + 7) % len(OLD_NPCS)]
    else:
        old_slots = [slot for slot in range(4) if slot not in npc_new_slots]
        old_before = _count_before(offset, lambda value: [slot for slot in range(4) if slot not in _new_npc_slots(value)])
        old_index = old_before + _rank_in_slots(old_slots, act_index)
        featured = OLD_NPCS[old_index % len(OLD_NPCS)]
        support = NEW_NPCS[(offset * 4 + act_index + 7) % len(NEW_NPCS)]

    lead = PARTY_IDS[(episode_number + act_index) % len(PARTY_IDS)]
    return lead, featured, support, primary, secondary


def fallback_episode(episode_number: int, tag_pairs: list[tuple[str, str]], rng) -> dict:
    acts = []
    episode_lead = PARTY_IDS[episode_number % len(PARTY_IDS)]
    for act_index, pair in enumerate(tag_pairs):
        lead, featured, support, primary, secondary = plan_entities(episode_number, act_index)
        # Keep a single through-line protagonist for each episode while letting
        # each act's supporting party member respond in their own voice.
        lead = episode_lead if act_index in (0, 3) else lead
        subplot_id = SUBPLOT_IDS[(episode_number + act_index) % len(SUBPLOT_IDS)]
        segments, act_title = make_narrative_segments(
            episode_number=episode_number,
            act_index=act_index,
            pair=pair,
            lead_id=lead,
            featured_npc_id=featured,
            support_npc_id=support,
            primary_place_id=primary,
            secondary_place_id=secondary,
            subplot_id=subplot_id,
            rng=rng,
        )
        decision = make_decision(
            episode_number=episode_number,
            act_index=act_index,
            pair=pair,
            lead_id=lead,
            featured_npc_id=featured,
            primary_place_id=primary,
            secondary_place_id=secondary,
            rng=rng,
        )
        acts.append({"id": f"act_{act_index + 1}", "title": act_title, "segments": segments, "decision": decision})

    title_templates = [
        "The Echo Beneath {primary}",
        "A Route Through {primary}",
        "The Promise at {primary}",
        "Between {primary} and {secondary}",
        "Where the Lattice Remembers",
        "The Signal No Map Holds",
        "A Safe Tone for One Night",
        "The Tether That Answered",
    ]
    first_lead = plan_entities(episode_number, 0)
    last_lead = plan_entities(episode_number, 3)
    primary_name = short_place(first_lead[3])
    secondary_name = short_place(last_lead[4])
    template = title_templates[stable_int(f"title:{episode_number}") % len(title_templates)]
    first_context = tag_context(tag_pairs[0][0], episode_number)
    last_context = tag_context(tag_pairs[-1][1], episode_number + 1)
    title = template.format(primary=primary_name, secondary=secondary_name)
    title = f"{title} — {first_context['concept'].title()} / {last_context['concept'].title()}"
    return {"id": f"ep_{episode_number:03d}", "title": title, "acts": acts}


def extract_json(text: str) -> dict | None:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        parsed = json.loads(cleaned)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            return None
        try:
            parsed = json.loads(cleaned[start : end + 1])
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None


def fix_id(raw, valid: set[str], name_map: dict[str, str]) -> str | None:
    if not raw:
        return None
    value = str(raw).strip()
    value = re.sub(r"\s*\([^)]*\)\s*$", "", value)
    if value in valid:
        return value
    return name_map.get(value.lower())


def clean_line(raw: object, default_character: str, default_place: str) -> dict:
    source = raw if isinstance(raw, dict) else {}
    character = (
        source.get("character")
        or source.get("char")
        or source.get("char_id")
        or source.get("speaker")
        or default_character
    )
    place = source.get("place") or source.get("place_id") or default_place
    dialogue = source.get("dialogue") or source.get("line") or source.get("text") or ""
    character = fix_id(character, VALID_CHAR_IDS, CHAR_NAME_TO_ID) or default_character
    place = fix_id(place, VALID_PLACE_IDS, PLACE_NAME_TO_ID) or default_place
    return line(character, place, str(dialogue), str(source.get("stage_directions", "") or ""))


def sanitize_api_episode(raw: dict, episode_number: int, pairs: list[tuple[str, str]], rng) -> dict | None:
    if not isinstance(raw, dict) or not isinstance(raw.get("acts"), list) or len(raw["acts"]) != 4:
        return None
    output = {"id": f"ep_{episode_number:03d}", "title": str(raw.get("title") or "Untitled resonance")[:160], "acts": []}
    for act_index, raw_act in enumerate(raw["acts"]):
        if not isinstance(raw_act, dict):
            return None
        raw_segments = raw_act.get("segments")
        if not isinstance(raw_segments, list):
            return None
        segments = []
        for segment in raw_segments:
            if not isinstance(segment, dict):
                return None
            if segment.get("type") == "tag":
                segments.append({"type": "tag", "tag": segment.get("tag")})
            elif segment.get("type") == "narrative":
                raw_lines = segment.get("lines", [])
                if not isinstance(raw_lines, list):
                    return None
                default_place = plan_entities(episode_number, act_index)[3]
                segments.append({
                    "type": "narrative",
                    "lines": [clean_line(item, "char_narrator", default_place) for item in raw_lines],
                })
            else:
                return None
        decision_raw = raw_act.get("decision")
        if not isinstance(decision_raw, dict):
            return None
        lead, featured, support, primary, secondary = plan_entities(episode_number, act_index)
        choices = []
        for choice_index, raw_choice in enumerate(decision_raw.get("choices", [])):
            if not isinstance(raw_choice, dict):
                return None
            subplot = raw_choice.get("subplot")
            if subplot not in VALID_SUBPLOT_IDS:
                subplot = SUBPLOT_IDS[(episode_number + act_index + choice_index) % len(SUBPLOT_IDS)]
            pass_raw = raw_choice.get("pass_outcome", {})
            fail_raw = raw_choice.get("fail_outcome", {})
            pass_outcome = pass_raw if isinstance(pass_raw, dict) else {}
            fail_outcome = fail_raw if isinstance(fail_raw, dict) else {}
            choices.append({
                "description": str(raw_choice.get("description") or "Investigate the resonance clue with the waiting crew"),
                "difficulty": str(raw_choice.get("difficulty") or ["easy", "medium", "hard"][choice_index % 3]),
                "subplot": subplot,
                "pass_outcome": {
                    "line": clean_line(pass_outcome.get("line"), lead, primary),
                    "subplot": subplot,
                    "delta": pass_outcome.get("delta", 1),
                },
                "fail_outcome": {
                    "line": clean_line(fail_outcome.get("line"), lead, primary),
                    "subplot": subplot,
                    "delta": fail_outcome.get("delta", -1),
                },
            })
        if len(choices) != 3:
            return None
        decision_line = clean_line(decision_raw.get("line"), lead, primary)
        output["acts"].append({
            "id": f"act_{act_index + 1}",
            "title": str(raw_act.get("title") or f"The {act_index + 1}th interval"),
            "segments": segments,
            "decision": {"line": decision_line, "choices": choices},
        })
    # Require the exact assignment, so a successful API response cannot quietly
    # skew the review distribution.
    actual_pairs = []
    for act in output["acts"]:
        actual = [segment.get("tag") for segment in act["segments"] if segment.get("type") == "tag"]
        actual_pairs.append(tuple(actual))
    if actual_pairs != pairs:
        return None
    return output


def build_prompts(episode_number: int, pairs: list[tuple[str, str]]) -> tuple[str, str]:
    planned = []
    for act_index, pair in enumerate(pairs):
        lead, featured, support, primary, secondary = plan_entities(episode_number, act_index)
        tag_details = []
        for tag_id in pair:
            context = tag_context(tag_id, episode_number + act_index)
            tag_details.append({
                "id": context["id"],
                "name": context["name"],
                "vocab_phrase": context["english"],
                "thai": context["thai"],
            })
        planned.append({
            "act": act_index + 1,
            "lead": lead,
            "npc": featured,
            "support_npc": support,
            "primary_place": primary,
            "secondary_place": secondary,
            "tags": tag_details,
        })
    system = f"""You write vivid, coherent episodes for the Thai language-learning RPG Chantara.
The world has floating skycities above a crystalline lattice that reacts to sound.
Return ONLY one JSON object; never use markdown or commentary.

Hard schema rules:
- id, title, and exactly four acts.
- Every act has id, title, a segments array, and decision.
- segments must be ordered narrative -> tag -> narrative -> tag -> narrative.
  The array is extensible, but this episode uses exactly the two assigned tags.
- Every narrative line has exactly character, place, dialogue, stage_directions.
- Use only the supplied IDs. Never put an ID such as char_malee in dialogue.
- Every decision has exactly three specific action choices, with easy, medium,
  and hard once each. Each choice has a concrete first-person pass and fail
  outcome, matching subplot IDs and deltas +1/+2 or 0/-1.
- Use the supplied vocabulary phrase naturally in the narrative immediately
  before its tag checkpoint; the vocabulary must matter to the scene, not be a
  glossary pasted onto it. Write about 12 narrative lines per act, roughly the
  length of the existing episodes.

Valid subplots: {', '.join(SUBPLOT_IDS)}"""
    user = f"""Write episode ep_{episode_number:03d}. Make the four acts one escalating story: discovery, pressure, crisis, and a practical aftermath. Feature the assigned NPCs and visit both assigned places in each act.

Assignments (use IDs exactly):
{json.dumps(planned, ensure_ascii=False, indent=2)}

For each tag, use its supplied English/Thai vocabulary in a natural spoken line immediately before the tag segment. Do not substitute tags. Output raw JSON only."""
    return system, user


def call_openrouter(api_key: str, model: str, system: str, user: str, retries: int = 3) -> str | None:
    if not api_key:
        return None
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 1.0,
        "max_tokens": 16000,
        "response_format": {"type": "json_object"},
    }
    request_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": REFERER,
        "X-Title": "Chantara staging content generator",
    }
    for attempt in range(retries):
        try:
            request = urllib.request.Request(API_URL, data=request_data, headers=headers, method="POST")
            with urllib.request.urlopen(request, timeout=180) as response:
                body = json.loads(response.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"]
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, KeyError, json.JSONDecodeError) as error:
            print(f"  OpenRouter attempt {attempt + 1} failed: {error}", file=sys.stderr)
            if attempt + 1 < retries:
                time.sleep(2 ** attempt)
    return None


def validate_generated_episode(episode: dict, expected_pairs: list[tuple[str, str]]) -> list[str]:
    errors = []
    if not episode.get("title") or len(episode.get("acts", [])) != 4:
        errors.append("episode must have a title and four acts")
        return errors
    for index, (act, expected) in enumerate(zip(episode["acts"], expected_pairs)):
        segments = act.get("segments")
        if not isinstance(segments, list):
            errors.append(f"act {index + 1} has no segments")
            continue
        actual = tuple(segment.get("tag") for segment in segments if segment.get("type") == "tag")
        if actual != expected:
            errors.append(f"act {index + 1} tags {actual} != {expected}")
        if len(actual) != 2 or segments[0].get("type") != "narrative" or segments[-1].get("type") != "narrative":
            errors.append(f"act {index + 1} has invalid narrative/tag pacing")
        if len(act.get("decision", {}).get("choices", [])) != 3:
            errors.append(f"act {index + 1} does not have three choices")
        for segment in segments:
            if segment.get("type") == "narrative":
                for line_item in segment.get("lines", []):
                    if not line_item.get("dialogue") or "[None]" in line_item.get("dialogue", "") or "char_" in line_item.get("dialogue", ""):
                        errors.append(f"act {index + 1} contains invalid narrative text")
    return errors


def generate_one(
    episode_number: int,
    pairs: list[tuple[str, str]],
    rng,
    *,
    api_key: str,
    model: str,
    offline: bool,
    require_openrouter: bool,
) -> tuple[dict, str]:
    if not offline and api_key:
        system, user = build_prompts(episode_number, pairs)
        for candidate_model in dict.fromkeys([model, FALLBACK_MODEL]):
            response = call_openrouter(api_key, candidate_model, system, user)
            if response:
                parsed = extract_json(response)
                if parsed:
                    sanitized = sanitize_api_episode(parsed, episode_number, pairs, rng)
                    if sanitized:
                        validation_errors = validate_generated_episode(sanitized, pairs)
                        if not validation_errors:
                            return sanitized, f"openrouter:{candidate_model}"
                        print(f"  rejected API episode: {'; '.join(validation_errors[:3])}", file=sys.stderr)
    if require_openrouter:
        raise RuntimeError(f"ep_{episode_number:03d} did not receive a valid OpenRouter response")
    return fallback_episode(episode_number, pairs, rng), "deterministic-fallback"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=170, help="number of episodes to add (default: 170)")
    parser.add_argument("--start", type=int, default=None, help="first episode number (default: after current data)")
    parser.add_argument("--seed", type=int, default=20260808, help="stable content seed")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenRouter model ID")
    parser.add_argument("--offline", action="store_true", help="skip OpenRouter and use the reviewed local writer")
    parser.add_argument(
        "--require-openrouter",
        action="store_true",
        help="fail instead of using local fallback when OpenRouter is unavailable or invalid",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="replace IDs in the requested --start/--count range (requires --start)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.count < 0:
        raise SystemExit("--count must be non-negative")
    if args.replace_existing and args.start is None:
        raise SystemExit("--replace-existing requires an explicit --start")
    if args.require_openrouter and args.offline:
        raise SystemExit("--require-openrouter and --offline cannot be used together")

    episodes = load(EPISODES_PATH)
    episode_numbers = [
        int(match.group(1))
        for episode in episodes
        if (match := re.fullmatch(r"ep_(\d+)", str(episode.get("id", ""))))
    ]
    start = args.start if args.start is not None else max(episode_numbers or [0]) + 1
    target = start + args.count
    if args.count == 0:
        print("Nothing to generate")
        return
    if args.replace_existing:
        episodes = [
            episode
            for episode in episodes
            if not (
                (match := re.fullmatch(r"ep_(\d+)", str(episode.get("id", ""))))
                and start <= int(match.group(1)) < target
            )
        ]

    existing_ids = {episode.get("id") for episode in episodes}
    api_key = "" if args.offline else __import__("os").environ.get("OPENROUTER_API_KEY", "")
    if args.require_openrouter and not api_key:
        raise SystemExit("OPENROUTER_API_KEY is required when --require-openrouter is set")
    if not args.offline and not api_key:
        print("OPENROUTER_API_KEY is not set; using the deterministic offline writer.", file=sys.stderr)
    usage = get_tag_usage(episodes)
    generated = 0
    modes = set()

    for episode_number in range(start, target):
        episode_id = f"ep_{episode_number:03d}"
        if episode_id in existing_ids:
            print(f"Skipping existing {episode_id}")
            continue
        rng = __import__("random").Random(args.seed + episode_number)
        pairs = choose_tag_pairs(usage, rng)
        # Reserve the slots only after a complete episode is ready. This makes
        # an interrupted run safe to resume and preserves least-used ordering.
        episode, mode = generate_one(
            episode_number,
            pairs,
            rng,
            api_key=api_key,
            model=args.model,
            offline=args.offline,
            require_openrouter=args.require_openrouter,
        )
        episode["id"] = episode_id
        validation_errors = validate_generated_episode(episode, pairs)
        if validation_errors:
            raise RuntimeError(f"{episode_id} failed generation validation: {'; '.join(validation_errors)}")
        episodes.append(episode)
        existing_ids.add(episode_id)
        for tag_id in (tag_id for pair in pairs for tag_id in pair):
            usage[tag_id] += 1
        generated += 1
        modes.add(mode)
        # Save after every successful episode, not after a large batch.
        EPISODES_PATH.write_text(json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[{generated}/{args.count}] {episode_id}: {episode['title']} ({mode})")

    print(f"Generated {generated} episodes; total {len(episodes)}")
    print(f"Generation modes: {', '.join(sorted(modes)) or 'none'}")
    print(f"Tag usage range after generation: {min(usage.values())}-{max(usage.values())}")


if __name__ == "__main__":
    main()
