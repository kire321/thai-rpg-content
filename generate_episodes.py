#!/usr/bin/env python3
"""
Generate N episodes for the Thai RPG CMS using the Kimi API.
Set N via environment variable: EPISODE_COUNT=10 python generate_episodes.py
"""

import json
import os
import random
import sys
import time

import requests

API_KEY = "sk-pnYuHsw8mrcgdcHdyVhEyUcRsxPa1Od7ZpFxeS2JMHdROhHk"
API_URL = "https://api.moonshot.ai/v1/chat/completions"
MODEL = "moonshot-v1-128k"


def load_data():
    with open("public/characters.json", "r", encoding="utf-8") as f:
        characters = json.load(f)
    with open("public/places.json", "r", encoding="utf-8") as f:
        places = json.load(f)
    with open("public/subplots.json", "r", encoding="utf-8") as f:
        subplots = json.load(f)
    with open("public/tags.json", "r", encoding="utf-8") as f:
        tags = json.load(f)
    with open("public/episodes.json", "r", encoding="utf-8") as f:
        episodes = json.load(f)
    return characters, places, subplots, tags, episodes


STORY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storytelling")


def build_context():
    with open(os.path.join(STORY_DIR, "world_building.md"), "r", encoding="utf-8") as f:
        world = f.read()
    with open(os.path.join(STORY_DIR, "characters.md"), "r", encoding="utf-8") as f:
        chars_md = f.read()
    with open(os.path.join(STORY_DIR, "places.md"), "r", encoding="utf-8") as f:
        places_md = f.read()
    with open(os.path.join(STORY_DIR, "recurring_subplots.md"), "r", encoding="utf-8") as f:
        subplots_md = f.read()
    return world, chars_md, places_md, subplots_md


def get_least_used_tags(tags, episodes, count=4):
    """Return the least-used tags across all episodes."""
    usage = {t["id"]: 0 for t in tags}
    for ep in episodes:
        for act in ep.get("acts", []):
            tag_id = act.get("tag", "")
            if tag_id in usage:
                usage[tag_id] += 1

    sorted_tags = sorted(tags, key=lambda t: (usage[t["id"]], random.random()))
    return sorted_tags[:count]


def get_template():
    return """
{
  "id": "ep_XXX",
  "title": "Episode Title Here",
  "acts": [
    {
      "id": "act_1",
      "title": "Act Title",
      "lines_before": [
        {"character": "char_...", "place": "place_...", "dialogue": "...", "stage_directions": "..."}
      ],
      "tag": "tag_XXX",
      "lines_after": [
        {"character": "char_...", "place": "place_...", "dialogue": "...", "stage_directions": "..."}
      ],
      "decision": {
        "line": {"character": "char_...", "place": "place_...", "dialogue": "...", "stage_directions": "..."},
        "choices": [
          {
            "description": "...",
            "difficulty": "easy|medium|hard",
            "subplot": "subplot_...",
            "pass_outcome": {
              "line": {"character": "char_...", "place": "place_...", "dialogue": "...", "stage_directions": "..."},
              "subplot": "subplot_...",
              "delta": 2
            },
            "fail_outcome": {
              "line": {"character": "char_...", "place": "place_...", "dialogue": "...", "stage_directions": "..."},
              "subplot": "subplot_...",
              "delta": -1
            }
          }
        ]
      }
    }
  ]
}
"""


def generate_episode(episode_num, assigned_tags, assigned_place, assigned_npcs, world, chars_md, places_md, subplots_md, existing_episodes_json):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    tag_descriptions = []
    for t in assigned_tags:
        # Get sample vocab from the tag
        sample_vocab = []
        for vid in t["vocab_item_ids"][:5]:
            v = next((v for v in json.load(open("public/vocab_items.json")) if v["id"] == vid), None)
            if v:
                sample_vocab.append(f"    - {v['english']}")
        tag_descriptions.append(
            f"Tag {t['id']} ({t['name']}):\n  Sample vocabulary phrases:\n" + "\n".join(sample_vocab)
        )

    system_prompt = """You are a narrative designer for a Thai language-learning RPG called Chantara.
Your task: Write ONE complete episode with 4 acts, in valid JSON format.

CRITICAL RULES:
1. Each act's TAG must be woven tightly into the narrative. The characters should USE the vocabulary phrases naturally in dialogue and stage directions. For example, if the tag is about "morning" phrases, the scene should take place at dawn, characters should discuss morning plans, wake up, etc.
2. Every line of dialogue should feel natural — characters using the vocabulary as real people would, not as language exercises.
3. Use ALL assigned characters and places throughout the episode.
4. Each decision choice must link to a different subplot.
5. Output ONLY valid JSON. No markdown code blocks, no explanations, no extra text.
6. All character IDs, place IDs, tag IDs, and subplot IDs must match exactly.
7. The episode must be consistent with the world of Chantara."""

    user_prompt = f"""Write episode #{episode_num} for the Thai RPG "Chantara" as valid JSON.

WORLD: Chantara is a world where an impassable crystalline lattice reacts to sound. Civilization survives on floating islands connected by resonance ships. Thai tonal language determines survival. Skycities include Khrueang (trade hub), Phrao (monastery), Tha Khwae (scavengers), Mae Rim (farms). Society: Tonal Orders (guilds), Listeners (monks who study lattice), Scavengers (surface dwellers), Groundless (political movement for surface living).

CHARACTERS:
- Party: char_chanida (Singer-in-training, hears hidden frequencies), char_pichit (ex-Listener monk with resonant staff), char_malee (scavenger engineer, crystal prosthetic leg), char_arthit (former ship captain, tattooed forbidden routes)
- NPCs: char_villager (ordinary islander), char_bandit (sky pirate with disruptor), char_merchant (trade negotiator), char_monk (Listener monk), char_scavenger (surface harvester), char_narrator (The Chronicler)

PLACES:
- place_khrueang_market (bustling market)
- place_anchor_spire (resonance anchor into lattice)
- place_phrao_monastery (Listener study center)
- place_lattice_surface (crystal ground)
- place_resonance_ship (ship deck between islands)
- place_tha_khwae_scrapyard (ship-breaking yard)
- place_the_hollow (cave with pre-Silencing ruins)
- place_mae_rim_gardens (hanging farm terraces)
- place_silent_zone (dead region, lattice unresponsive)
- place_tonal_archives (library of safe routes)

SUBPLOTS: subplot_frequency_map (Chanida's open map), subplot_haunted_ship (Arthit's lost ship echoes), subplot_crystal_leg (Malee's prosthetic resonance), subplot_listener_warning (Pichit's dismissed lattice warning), subplot_groundless (surface colonization movement)

ASSIGNED FOR THIS EPISODE:
Place: {assigned_place['id']} ({assigned_place['name']})
NPCs: {', '.join([f"{n['id']} ({n['name']})" for n in assigned_npcs])}
Tags:
{'\n'.join(tag_descriptions)}

TEMPLATE:
{get_template()}

RULES:
- 4 acts: Introduce challenge → Escalate → Crisis → Transform (avoid cheesy moral endings)
- Each act: 5-7 lines_before, TAG, 3-4 lines_after, decision with 3 choices
- NATURALLY weave tag vocabulary into dialogue. If tag is "morning", characters should talk about dawn, waking up, morning plans
- Choices link to different subplots. Difficulty: easy/medium/hard. Pass: +1 to +3 delta. Fail: 0 to -2 delta
- Use char_narrator for scene transitions
- Output ONLY JSON, no markdown, no explanation

Write JSON:"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 12000,
        "temperature": 1
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"  API error: {response.status_code} - {response.text[:300]}")
        return None

    content = response.json()["choices"][0]["message"]["content"]

    # Clean up
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        episode = json.loads(content)
        return episode
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        # Save raw for debugging
        with open(f"/tmp/ep_{episode_num}_raw.txt", "w") as f:
            f.write(content)
        print(f"  Raw saved to /tmp/ep_{episode_num}_raw.txt")
        return None


def validate_episode_structure(episode, tag_ids, char_ids, place_ids, subplot_ids):
    """Basic structural validation of a generated episode."""
    errors = []

    if not episode.get("id"):
        errors.append("Missing episode id")
    if not episode.get("title"):
        errors.append("Missing episode title")
    if len(episode.get("acts", [])) != 4:
        errors.append(f"Expected 4 acts, got {len(episode.get('acts', []))}")

    for act in episode.get("acts", []):
        if not act.get("tag") or act["tag"] not in tag_ids:
            errors.append(f"Act {act.get('id', '?')} has invalid tag: {act.get('tag')}")

        for line in act.get("lines_before", []) + act.get("lines_after", []):
            if line.get("character") not in char_ids:
                errors.append(f"Invalid character: {line.get('character')}")
            if line.get("place") not in place_ids:
                errors.append(f"Invalid place: {line.get('place')}")

        dec = act.get("decision", {})
        for choice in dec.get("choices", []):
            if choice.get("subplot") not in subplot_ids:
                errors.append(f"Invalid subplot in choice: {choice.get('subplot')}")
            for outcome_key in ["pass_outcome", "fail_outcome"]:
                outcome = choice.get(outcome_key, {})
                if outcome.get("subplot") not in subplot_ids:
                    errors.append(f"Invalid subplot in {outcome_key}: {outcome.get('subplot')}")
                line = outcome.get("line", {})
                if line.get("character") not in char_ids:
                    errors.append(f"Invalid character in {outcome_key}: {line.get('character')}")
                if line.get("place") not in place_ids:
                    errors.append(f"Invalid place in {outcome_key}: {line.get('place')}")

    return errors


def main():
    n = int(os.environ.get("EPISODE_COUNT", "1"))
    print(f"Generating {n} episode(s)...")

    characters, places, subplots, tags, episodes = load_data()
    world, chars_md, places_md, subplots_md = build_context()

    char_ids = set(c["id"] for c in characters)
    place_ids = set(p["id"] for p in places)
    subplot_ids = set(s["id"] for s in subplots)
    tag_ids = set(t["id"] for t in tags)

    npcs = [c for c in characters if c["type"] == "npc"]
    party = [c for c in characters if c["type"] == "party"]

    existing_json = json.dumps(episodes, ensure_ascii=False, indent=2)

    generated = 0
    failed = 0
    start_ep = len(episodes) + 1

    for i in range(n):
        ep_num = start_ep + i
        print(f"\n--- Generating episode {ep_num} ({i+1}/{n}) ---")

        # Assign least-used tags
        assigned_tags = get_least_used_tags(tags, episodes, count=4)
        assigned_place = random.choice(places)
        assigned_npcs = random.sample(npcs, k=min(2, len(npcs)))

        print(f"  Tags: {[t['id'] for t in assigned_tags]}")
        print(f"  Place: {assigned_place['id']}")
        print(f"  NPCs: {[n['id'] for n in assigned_npcs]}")

        episode = generate_episode(
            ep_num, assigned_tags, assigned_place, assigned_npcs,
            world, chars_md, places_md, subplots_md, existing_json
        )

        if episode is None:
            failed += 1
            time.sleep(2)
            continue

        # Validate structure
        errors = validate_episode_structure(episode, tag_ids, char_ids, place_ids, subplot_ids)
        if errors:
            print(f"  Validation errors: {len(errors)}")
            for e in errors:
                print(f"    - {e}")
            failed += 1
            time.sleep(2)
            continue

        # Fix episode ID
        episode["id"] = f"ep_{ep_num:03d}"

        # Ensure act IDs are correct
        for j, act in enumerate(episode["acts"]):
            act["id"] = f"act_{j+1}"

        episodes.append(episode)
        generated += 1
        print(f"  Generated: {episode['id']} - {episode['title']}")

        # Save after each successful generation
        with open("public/episodes.json", "w", encoding="utf-8") as f:
            json.dump(episodes, f, ensure_ascii=False, indent=2)

        time.sleep(1)

    print(f"\n=== Done ===")
    print(f"Generated: {generated}, Failed: {failed}")
    print(f"Total episodes: {len(episodes)}")

    # Tag usage summary
    usage = {}
    for ep in episodes:
        for act in ep.get("acts", []):
            tid = act.get("tag", "")
            usage[tid] = usage.get(tid, 0) + 1

    used_once = sum(1 for v in usage.values() if v == 1)
    used_multiple = sum(1 for v in usage.values() if v > 1)
    unused = len(tags) - len(usage)
    print(f"Tags used once: {used_once}")
    print(f"Tags used multiple times: {used_multiple}")
    print(f"Tags unused: {unused}")


if __name__ == "__main__":
    main()
