#!/usr/bin/env python3
"""
Generate 170 new episodes (ep_341 to ep_510) using OpenRouter API.
Each episode has 4 acts, each with 2 tags (new segments format).
"""

import json
import os
import random
import re
import sys
import time
from pathlib import Path

# --- Configuration ---
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat-v3-0324"

APP_DIR = Path(__file__).parent
EPISODES_FILE = APP_DIR / "public" / "episodes.json"
TAGS_FILE = APP_DIR / "public" / "tags.json"
CHARACTERS_FILE = APP_DIR / "public" / "characters.json"
PLACES_FILE = APP_DIR / "public" / "places.json"
SUBPLOTS_FILE = APP_DIR / "public" / "subplots.json"

# --- Load reference data ---
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

all_episodes = load_json(EPISODES_FILE)
tags_data = load_json(TAGS_FILE)
characters_data = load_json(CHARACTERS_FILE)
places_data = load_json(PLACES_FILE)
subplots_data = load_json(SUBPLOTS_FILE)

VALID_CHAR_IDS = {c["id"] for c in characters_data}
VALID_PLACE_IDS = {p["id"] for p in places_data}
VALID_SUBPLOT_IDS = {s["id"] for s in subplots_data}
VALID_TAG_IDS = {t["id"] for t in tags_data}

# Character name to ID mapping (for sanitizing LLM output)
CHAR_NAME_MAP = {}
for c in characters_data:
    CHAR_NAME_MAP[c["name"].lower()] = c["id"]
    # Also map first name
    CHAR_NAME_MAP[c["name"].lower().split()[0]] = c["id"]

# Place name to ID mapping
PLACE_NAME_MAP = {}
for p in places_data:
    PLACE_NAME_MAP[p["name"].lower()] = p["id"]

# Tag name to ID mapping
TAG_NAME_MAP = {}
for t in tags_data:
    TAG_NAME_MAP[t["name"].lower()] = t["id"]

SUBPLOT_LIST = list(VALID_SUBPLOT_IDS)

# --- Tag distribution: least-used-first ---
def get_tag_usage():
    """Count how many times each tag is used across all episodes."""
    usage = {t["id"]: 0 for t in tags_data}
    for ep in all_episodes:
        for act in ep.get("acts", []):
            # Old format
            if "tag" in act:
                tag = act["tag"]
                if tag in usage:
                    usage[tag] += 1
            # New format
            for seg in act.get("segments", []):
                if isinstance(seg, dict) and seg.get("type") == "tag":
                    tag = seg.get("tag", "")
                    if tag in usage:
                        usage[tag] += 1
    return usage

# --- Prompt construction ---

CHOICE_TEMPLATES = [
    "Convince {{char}} to help",
    "Sneak past {{char}} undetected",
    "Attack {{char}} directly",
    "Offer {{char}} a trade",
    "Ask {{char}} for information",
    "Follow {{char}} secretly",
    "Help {{char}} with their problem",
    "Challenge {{char}}'s beliefs",
    "Use resonance on {{char}}",
    "Try to escape from {{char}}",
    "Negotiate with {{char}}",
    "Reveal a secret to {{char}}",
    "Threaten {{char}}",
    "Pretend to agree with {{char}}",
    "Search the area while {{char}} is distracted",
]

def build_system_prompt(valid_chars, valid_places, valid_subplots):
    return f"""You are a Thai RPG episode writer. Write episodes in valid JSON format.

STRICT RULES:
1. Use ONLY these character IDs: {', '.join(sorted(VALID_CHAR_IDS))}
2. Use ONLY these place IDs: {', '.join(sorted(VALID_PLACE_IDS))}
3. Use ONLY these subplot IDs: {', '.join(sorted(VALID_SUBPLOT_IDS))}
4. NEVER invent new IDs. NEVER use character names as IDs. NEVER add parenthetical notes to IDs.
5. Each act's segments array must alternate: narrative → tag → narrative → tag → narrative
6. The decision must have exactly 3 choices with difficulties: one easy, one medium, one hard
7. Each choice must have pass_outcome and fail_outcome with: line (character, place, dialogue, stage_directions), subplot (from valid list), delta (-2, -1, 0, 1, or 2)
8. Character IDs must be EXACTLY as listed above - never "char_017(Ratana)" or "char_ratana" - just the exact ID from the list
9. subplot field must be exactly one of: {', '.join(sorted(VALID_SUBPLOT_IDS))} - never "None" or null
10. place field in lines must be exactly one of: {', '.join(sorted(VALID_PLACE_IDS)[:10])} etc.
11. NEVER use markdown code blocks in your response. Output raw JSON only.
12. Do NOT include comments in the JSON.
"""

def build_user_prompt(episode_num, tag_assignment, assigned_subplot, existing_episodes_summary):
    ep_id = f"ep_{{episode_num:03d}}"
    
    # Pick 2-3 random characters for this episode
    party_chars = [c for c in characters_data if c["type"] == "party"]
    npc_chars = [c for c in characters_data if c["type"] == "npc"]
    ep_chars = random.sample(party_chars, min(2, len(party_chars))) + random.sample(npc_chars, min(2, len(npc_chars)))
    char_ids = [c["id"] for c in ep_chars]
    
    # Pick 2 random places
    ep_places = random.sample(places_data, min(2, len(places_data)))
    place_ids = [p["id"] for p in ep_places]
    
    # Show the tag names
    tag_lines = []
    for act_idx, (t1, t2) in enumerate(tag_assignment):
        t1_name = next((t["name"] for t in tags_data if t["id"] == t1), t1)
        t2_name = next((t["name"] for t in tags_data if t["id"] == t2), t2)
        tag_lines.append(f"  Act {act_idx+1}: '{t1}' ({t1_name}) + '{t2}' ({t2_name})")
    
    return f"""Write Thai RPG episode {ep_id} in the NEW FORMAT with 4 acts, each having 2 tags.

TAG ASSIGNMENT (you MUST use ALL of these tags exactly as assigned):
{chr(10).join(tag_lines)}

SUBPLOT: {assigned_subplot}

CHARACTERS TO FEATURE: {', '.join(char_ids)}
PLACES: {', '.join(place_ids)}

EPISODE STRUCTURE - NEW FORMAT:
Each act uses this segments array (NOT lines_before/tag/lines_after):
```
"segments": [
  {{"type": "narrative", "lines": [{{"character": "CHAR_ID", "place": "PLACE_ID", "dialogue": "...", "stage_directions": ""}}]}},
  {{"type": "tag", "tag": "tag_XXX"}},
  {{"type": "narrative", "lines": [...]}},
  {{"type": "tag", "tag": "tag_XXX"}},
  {{"type": "narrative", "lines": [...]}}
]
```

DECISION FORMAT (3 choices, one easy, one medium, one hard):
```
"decision": {{
  "line": {{"character": "...", "place": "...", "dialogue": "What do you do?", "stage_directions": ""}},
  "choices": [
    {{"description": "...", "difficulty": "easy", "subplot": "{assigned_subplot}", "pass_outcome": {{"line": {{...}}, "subplot": "{assigned_subplot}", "delta": 1}}, "fail_outcome": {{"line": {{...}}, "subplot": "{assigned_subplot}", "delta": -1}}}},
    {{"description": "...", "difficulty": "medium", "subplot": "{assigned_subplot}", "pass_outcome": {{...}}, "fail_outcome": {{...}}}},
    {{"description": "...", "difficulty": "hard", "subplot": "{assigned_subplot}", "pass_outcome": {{...}}, "fail_outcome": {{...}}}}
  ]
}}
```

Write episode {ep_id} as valid JSON with this structure:
```json
{{
  "id": "{ep_id}",
  "title": "Descriptive Title",
  "acts": [
    {{
      "id": "act_001",
      "title": "Act Title",
      "segments": [...],
      "decision": {{...}}
    }},
    ...4 acts total
  ]
}}
```

IMPORTANT: 
- Use EXACTLY the tag IDs assigned above - do NOT substitute
- Output ONLY the JSON, no markdown code blocks, no explanation
- All character IDs must be from: {', '.join(sorted(VALID_CHAR_IDS))}
- All place IDs must be from: {', '.join(sorted(VALID_PLACE_IDS))}
- subplot must be exactly: {assigned_subplot}
"""

# --- API call ---
import urllib.request
import urllib.error

def call_api(messages, max_retries=3):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://thai-rpg-cms.local",
        "X-Title": "Thai RPG CMS",
    }
    data = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 8000,
    }).encode('utf-8')
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"  API attempt {attempt+1} failed: {e}")
            time.sleep(2 ** attempt)
    return None

# --- Parse and sanitize ---
def extract_json(text):
    """Extract JSON from the LLM response, handling code blocks."""
    # Try to find JSON in code blocks
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
    # Try to find raw JSON object
    match = re.search(r'(\{.*\})', text, re.DOTALL)
    if match:
        return match.group(1)
    return text

def sanitize_id(raw_id, valid_set, name_map=None):
    """Fix common LLM ID mistakes."""
    if not raw_id:
        return None
    
    raw = str(raw_id).strip()
    
    # Remove parenthetical notes: "char_017(Ratana)" → "char_017"
    raw = re.sub(r'\s*\([^)]*\)\s*$', '', raw)
    
    # Direct match
    if raw in valid_set:
        return raw
    
    # Name map lookup
    if name_map:
        lowered = raw.lower()
        if lowered in name_map:
            return name_map[lowered]
    
    return raw  # Return as-is, will be caught by validation

def fix_character_id(raw_id):
    """Fix character IDs with comprehensive mapping."""
    result = sanitize_id(raw_id, VALID_CHAR_IDS, CHAR_NAME_MAP)
    if result in VALID_CHAR_IDS:
        return result
    # Additional fixes for common LLM mistakes
    fixes = {
        "char_narrator": "char_narrator",
        "char_listener_monk": "char_monk",
        "char_singer_echo": "char_chanida",
        "char_cartographer": "char_ampa",
        "char_inquisitor": "char_kamon",
        "char_tam": "char_thanet",
        "char_groundless": "char_prayut",
        "char_lead_enforcer": "char_kamon",
    }
    return fixes.get(result, result)

def fix_place_id(raw_id):
    """Fix place IDs."""
    result = sanitize_id(raw_id, VALID_PLACE_IDS, PLACE_NAME_MAP)
    if result in VALID_PLACE_IDS:
        return result
    fixes = {
        "place_thakwae_scrapyard": "place_tha_khwae_scrapyard",
    }
    return fixes.get(result, result)

def fix_subplot_id(raw_id):
    """Fix subplot IDs."""
    if not raw_id or str(raw_id).lower() in ("none", "null", ""):
        return random.choice(SUBPLOT_LIST)
    result = str(raw_id).strip()
    if result in VALID_SUBPLOT_IDS:
        return result
    return random.choice(SUBPLOT_LIST)

def fix_tag_id(raw_id):
    """Fix tag IDs."""
    result = sanitize_id(raw_id, VALID_TAG_IDS, TAG_NAME_MAP)
    if result in VALID_TAG_IDS:
        return result
    return None

def sanitize_episode(ep, expected_tags):
    """Sanitize an episode to fix common LLM errors."""
    fixes_log = []
    
    for act in ep.get("acts", []):
        # Fix segments
        for seg in act.get("segments", []):
            if seg.get("type") == "narrative":
                for line in seg.get("lines", []):
                    old_char = line.get("character", "")
                    new_char = fix_character_id(old_char)
                    if old_char != new_char:
                        line["character"] = new_char
                        if old_char != new_char:
                            fixes_log.append(f"char: {old_char} → {new_char}")
                    
                    old_place = line.get("place", "")
                    new_place = fix_place_id(old_place)
                    if old_place != new_place:
                        line["place"] = new_place
                        fixes_log.append(f"place: {old_place} → {new_place}")
            
            elif seg.get("type") == "tag":
                old_tag = seg.get("tag", "")
                new_tag = fix_tag_id(old_tag)
                if new_tag and old_tag != new_tag:
                    seg["tag"] = new_tag
                    fixes_log.append(f"tag: {old_tag} → {new_tag}")
        
        # Fix decision
        decision = act.get("decision", {})
        if decision:
            for line in [decision.get("line", {})]:
                if line:
                    old_char = line.get("character", "")
                    new_char = fix_character_id(old_char)
                    if old_char != new_char:
                        line["character"] = new_char
            
            for choice in decision.get("choices", []):
                old_sub = choice.get("subplot", "")
                new_sub = fix_subplot_id(old_sub)
                if old_sub != new_sub:
                    choice["subplot"] = new_sub
                    fixes_log.append(f"subplot: {old_sub} → {new_sub}")
                
                for outcome_key in ["pass_outcome", "fail_outcome"]:
                    outcome = choice.get(outcome_key, {})
                    if outcome:
                        old_sub = outcome.get("subplot", "")
                        new_sub = fix_subplot_id(old_sub)
                        if old_sub != new_sub:
                            outcome["subplot"] = new_sub
                        
                        line = outcome.get("line", {})
                        if line:
                            old_char = line.get("character", "")
                            new_char = fix_character_id(old_char)
                            if old_char != new_char:
                                line["character"] = new_char
    
    return ep, fixes_log

def validate_episode(ep, expected_num_tags=8):
    """Validate an episode structure. Returns (is_valid, errors)."""
    errors = []
    
    if "id" not in ep or "title" not in ep or "acts" not in ep:
        return False, ["Missing required fields"]
    
    if len(ep.get("acts", [])) != 4:
        errors.append(f"Expected 4 acts, got {len(ep.get('acts', []))}")
    
    tag_count = 0
    for act in ep.get("acts", []):
        if "segments" not in act:
            errors.append(f"Act {act.get('id', '?')} missing segments")
            continue
        
        segments = act.get("segments", [])
        if len(segments) != 5:
            errors.append(f"Act {act.get('id', '?')} expected 5 segments, got {len(segments)}")
        
        for seg in segments:
            if seg.get("type") == "narrative":
                for line in seg.get("lines", []):
                    char_id = line.get("character", "")
                    if char_id not in VALID_CHAR_IDS:
                        errors.append(f"Invalid character: {char_id}")
                    place_id = line.get("place", "")
                    if place_id not in VALID_PLACE_IDS:
                        errors.append(f"Invalid place: {place_id}")
            elif seg.get("type") == "tag":
                tag_id = seg.get("tag", "")
                if tag_id not in VALID_TAG_IDS:
                    errors.append(f"Invalid tag: {tag_id}")
                tag_count += 1
            else:
                errors.append(f"Unknown segment type: {seg.get('type')}")
        
        decision = act.get("decision", {})
        if decision:
            choices = decision.get("choices", [])
            if len(choices) != 3:
                errors.append(f"Act {act.get('id', '?')} expected 3 choices, got {len(choices)}")
            for choice in choices:
                sub = choice.get("subplot", "")
                if sub not in VALID_SUBPLOT_IDS:
                    errors.append(f"Invalid subplot in choice: {sub}")
                for outcome_key in ["pass_outcome", "fail_outcome"]:
                    outcome = choice.get(outcome_key, {})
                    if outcome:
                        sub = outcome.get("subplot", "")
                        if sub not in VALID_SUBPLOT_IDS:
                            errors.append(f"Invalid subplot in {outcome_key}: {sub}")
    
    if tag_count != expected_num_tags:
        errors.append(f"Expected {expected_num_tags} tags, found {tag_count}")
    
    return len(errors) == 0, errors

# --- Main generation ---
def generate_episode(episode_num, tag_assignment, assigned_subplot):
    """Generate a single episode via OpenRouter API."""
    system_prompt = build_system_prompt(VALID_CHAR_IDS, VALID_PLACE_IDS, VALID_SUBPLOT_IDS)
    user_prompt = build_user_prompt(episode_num, tag_assignment, assigned_subplot, "")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    response = call_api(messages)
    if not response:
        return None, "API call failed"
    
    json_str = extract_json(response)
    
    try:
        episode = json.loads(json_str)
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"
    
    # Sanitize
    episode, fixes = sanitize_episode(episode, tag_assignment)
    
    # Validate
    is_valid, errors = validate_episode(episode)
    if not is_valid:
        return None, f"Validation errors: {'; '.join(errors)}"
    
    return episode, None

def get_least_used_tags(usage, count):
    """Get the least-used tags."""
    sorted_tags = sorted(usage.items(), key=lambda x: x[1])
    return [t[0] for t in sorted_tags[:count]]

def main():
    if not API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set")
        sys.exit(1)
    
    usage = get_tag_usage()
    
    # Determine which episodes to generate
    start_num = len(all_episodes) + 1
    target_count = 510
    
    if start_num > target_count:
        print(f"Already have {len(all_episodes)} episodes. Nothing to generate.")
        return
    
    to_generate = target_count - len(all_episodes)
    print(f"Have {len(all_episodes)} episodes. Generating {to_generate} more (ep_{start_num:03d} to ep_{target_count:03d})")
    
    generated = []
    
    for ep_num in range(start_num, target_count + 1):
        ep_id = f"ep_{{ep_num:03d}}"
        print(f"\nGenerating {ep_id}...")
        
        # Get 8 least-used tags for this episode (2 per act × 4 acts)
        tag_pool = get_least_used_tags(usage, 8)
        
        # Assign 2 tags per act
        tag_assignment = [
            (tag_pool[0], tag_pool[1]),
            (tag_pool[2], tag_pool[3]),
            (tag_pool[4], tag_pool[5]),
            (tag_pool[6], tag_pool[7]),
        ]
        
        # Update usage
        for t in tag_pool[:8]:
            usage[t] += 1
        
        # Pick a subplot
        assigned_subplot = random.choice(SUBPLOT_LIST)
        
        # Generate
        episode, error = generate_episode(ep_num, tag_assignment, assigned_subplot)
        
        if episode:
            # Ensure correct ID
            episode["id"] = ep_id
            generated.append(episode)
            all_episodes.append(episode)
            print(f"  ✓ Generated {ep_id}: {episode['title']}")
            
            # Save progress every 10 episodes
            if len(generated) % 10 == 0:
                with open(EPISODES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(all_episodes, f, indent=2, ensure_ascii=False)
                print(f"  💾 Saved progress ({len(all_episodes)} total episodes)")
        else:
            print(f"  ✗ Failed: {error}")
            # Retry once
            print(f"  🔄 Retrying {ep_id}...")
            time.sleep(5)
            episode, error = generate_episode(ep_num, tag_assignment, assigned_subplot)
            if episode:
                episode["id"] = ep_id
                generated.append(episode)
                all_episodes.append(episode)
                print(f"  ✓ Generated {ep_id} on retry: {episode['title']}")
            else:
                print(f"  ✗ Retry failed: {error}")
        
        time.sleep(1)  # Rate limiting
    
    # Final save
    with open(EPISODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_episodes, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Done! Generated {len(generated)} new episodes.")
    print(f"Total episodes: {len(all_episodes)}")

if __name__ == "__main__":
    main()
