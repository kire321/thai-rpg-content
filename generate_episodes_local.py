#!/usr/bin/env python3
"""
Generate 170 new episodes locally using template-based narrative generation.
Each episode has 4 acts with 2 tags each (new segments format).
"""

import json
import random
from pathlib import Path

APP_DIR = Path(__file__).parent
EPISODES_FILE = APP_DIR / "public" / "episodes.json"
TAGS_FILE = APP_DIR / "public" / "tags.json"
CHARACTERS_FILE = APP_DIR / "public" / "characters.json"
PLACES_FILE = APP_DIR / "public" / "places.json"
SUBPLOTS_FILE = APP_DIR / "public" / "subplots.json"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

all_episodes = load_json(EPISODES_FILE)
tags_data = load_json(TAGS_FILE)
characters_data = load_json(CHARACTERS_FILE)
places_data = load_json(PLACES_FILE)
subplots_data = load_json(SUBPLOTS_FILE)

VALID_CHAR_IDS = [c["id"] for c in characters_data]
VALID_PLACE_IDS = [p["id"] for p in places_data]
VALID_SUBPLOT_IDS = [s["id"] for s in subplots_data]
party_chars = [c for c in characters_data if c["type"] == "party"]
npc_chars = [c for c in characters_data if c["type"] == "npc"]
narrator = [c for c in characters_data if c["type"] == "narrator"][0]

# Character personality dialogue styles
CHAR_VOICES = {
    "char_chanida": ["I can hear it... the lattice is singing.", "The Tonal Orders are hiding something from us.", "Let me try a different frequency.", "This resonance... it's beautiful and terrifying."],
    "char_pichit": ["The lattice teaches patience.", "My staff resonates with this place.", "There is wisdom in silence.", "We must consider the consequences."],
    "char_malee": ["I can fix this. Probably.", "Watch your step. This platform's seen better days.", "Surface folk know things skycity people don't.", "That engine needs scavenged parts. I know where to find them."],
    "char_arthit": ["I've seen this before. It doesn't end well.", "My maps show a safe route. Maybe.", "The lattice surges are getting worse.", "I won't lose another crew. Not again."],
    "char_ratana": ["The object tells a story... of fear and longing.", "I see echoes where others see only shadows.", "The Archives hold truths the Orders fear.", "Touch this and tell me what you feel."],
    "char_kamon": ["Stand aside. I have a job to do.", "My armor absorbs the surge. Your move.", "I've silenced too many. Don't make me add you.", "The Orders cast me out. Their mistake."],
    "char_bussaba": ["This bloom responds to the C-sharp tone.", "My gardens can heal resonance sickness, you know.", "The plants remember what the people forgot.", "Touch it gently. It senses your intention."],
    "char_thanet": ["I can feel the path! It's this way!", "The lattice is... happy here. Is that weird?", "I don't need instruments. I just... know.", "Can we stay a little longer? Please?"],
    "char_suda": ["My city fell. I alone survived.", "The core fragment speaks to me. It remembers.", "Sri Thep is real. I can take you there.", "Don't pity me. Pity those who caused it."],
    "char_prayut": ["The skycities are parasites, I tell you.", "This device will sever their tether.", "You think I'm mad? Wait until you see the truth.", "I build what the Orders fear most."],
    "char_duangjai": ["Your single-tone approach is... limited.", "Listen to the harmonics. All of them at once.", "My tradition predates the Orders by centuries.", "Layer upon layer, until the pattern emerges."],
    "char_somsak": ["I have what you need. The price is fair.", "My informants see everything. For a price.", "That official? Bribable. His assistant? Not so much.", "Smuggling is just... creative logistics."],
    "char_niran": ["In silence, truth reveals itself.", "The lattice whispers constantly. Can you not hear it?", "Shield your mind. Breathe. Let go.", "I have achieved what the Orders only theorize about."],
    "char_ampa": ["My maps show the lattice is expanding.", "This geometry shouldn't be possible. And yet...", "The Orders arrested my mentor for mapping truth.", "Every measurement confirms it. The lattice is growing."],
}

# Stage direction templates
STAGE_TEMPLATES = [
    "{} looks around nervously.",
    "The lattice hums beneath {}'s feet.",
    "{} pauses, listening to something only they can hear.",
    "A distant resonance echoes through the chamber.",
    "{} raises a hand defensively.",
    "Crystal formations flicker with inner light.",
    "{}'s expression shifts from concern to determination.",
    "The ambient tone shifts to a minor key.",
    "{} studies their surroundings carefully.",
    "A vibration ripples through the platform.",
    "{} takes a deep breath and continues.",
    "The air thickens with harmonic pressure.",
    "{}'s eyes widen at what they see.",
    "Resonance dust sparkles in the air.",
    "{} reaches for their equipment.",
    "A low frequency rumble builds from below.",
    "{} exchanges a look with their companion.",
    "The temperature drops suddenly.",
    "{} steps forward cautiously.",
    "Harmonic patterns dance across the walls.",
]

# Narrative line templates
NARRATIVE_TEMPLATES = [
    "The {} stretches out before you, its {} glowing faintly in the dim light.",
    "You arrive at the {}. {} is already there, waiting.",
    "The journey to the {} took longer than expected. The lattice currents are unpredictable today.",
    "{} leads the way through the {}, their footsteps echoing against the crystal walls.",
    "A sudden resonance surge shakes the {}. {} braces against a pillar.",
    "The {} is busier than usual. {} pushes through the crowd toward you.",
    "From the edge of the {}, you can see the lattice stretching to the horizon.",
    "{} examines the ancient markings in the {} with growing excitement.",
    "The {} falls silent as you enter. {} stands at the center, eyes closed in meditation.",
    "A messenger finds you at the {}. {} needs to see you urgently.",
    "The {} holds secrets that the Tonal Orders would kill to protect.",
    "{} discovered something in the {} that changes everything.",
    "The air at the {} tastes of ozone and old resonance.",
    "{} waits for you in the shadows of the {}, hood pulled low.",
    "The {} responds to your presence, crystal formations shifting subtly.",
    "{}'s voice carries a warning note as you approach the {}.",
    "The {} has changed since your last visit. {} notices it too.",
    "Something ancient stirs in the depths of the {}.",
    "{} points toward a passage in the {} that wasn't there before.",
    "The {} remembers. The question is whether you want to hear what it has to say.",
]

# Decision prompts
DECISION_PROMPTS = [
    "What do you do?",
    "How do you respond?",
    "What is your next move?",
    "You must decide quickly.",
    "The choice is yours.",
    "Time is running out. What do you do?",
    "Every option carries risk. Choose carefully.",
    "The lattice awaits your decision.",
]

# Choice descriptions
CHOICE_TEMPLATES = [
    ("Convince {{char}} to see reason", "medium"),
    ("Sneak past {{char}} undetected", "hard"),
    ("Confront {{char}} directly", "easy"),
    ("Offer {{char}} a compromise", "medium"),
    ("Ask {{char}} what they really want", "easy"),
    ("Follow {{char}} without being seen", "hard"),
    ("Help {{char}} with their problem", "easy"),
    ("Challenge {{char}}'s assumptions", "medium"),
    ("Use resonance to influence {{char}}", "hard"),
    ("Try to escape before {{char}} notices", "hard"),
    ("Negotiate a deal with {{char}}", "medium"),
    ("Reveal what you know to {{char}}", "easy"),
    ("Bluff your way past {{char}}", "hard"),
    ("Wait and see what {{char}} does next", "easy"),
    ("Search for another way around {{char}}", "medium"),
    ("Appeal to {{char}}'s better nature", "medium"),
    ("Threaten {{char}} if they don't cooperate", "hard"),
    ("Pretend to agree with {{char}}", "hard"),
]

# Outcome line templates
PASS_LINES = [
    "It works. {} relaxes, and the tension drains from the scene.",
    "Success. {} nods approvingly at your approach.",
    "The gamble pays off. {} is impressed by your skill.",
    "Perfect execution. {} offers their help willingly.",
    "Your instincts were right. {} reveals valuable information.",
]

FAIL_LINES = [
    "It doesn't work. {} sees through your attempt immediately.",
    "The approach backfires. {} becomes more suspicious.",
    "A miscalculation. {} reacts defensively, making things worse.",
    "The attempt fails spectacularly. {} will remember this.",
    "Too risky. {} sees the danger and retreats before you can explain.",
]

# Episode title templates
TITLE_TEMPLATES = [
    "The {} {}",
    "{} of the {}",
    "{} and the {}",
    "Through the {}",
    "The Last {}",
    "Echoes of {}",
    "Beneath the {}",
    "The {} Resonance",
    "Whispers in the {}",
    "The {} Gambit",
    "Shadows of the {}",
    "The {} Awakening",
    "Song of the {}",
    "The {} Tether",
    "Fragments of {}",
    "The {} Sacrifice",
    "Rites of {}",
    "The {} Threshold",
    "Visions of {}",
    "The {} Covenant",
]

TITLE_NOUNS = [
    "Crystal", "Lattice", "Resonance", "Echo", "Frequency", "Tone", "Harmonic",
    "Singer", "Monk", "Scavenger", "Pirate", "Garden", "Archive", "Ship",
    "Storm", "Silence", "Whisper", "Dream", "Star", "Void", "Flame", "Tide",
    "Peak", "Depth", "Vale", "Spire", "Bridge", "Haven", "Ruin", "Mist",
    "Dawn", "Dusk", "Thunder", "Frost", "Ember", "Shard", "Veil", "Rift",
]

TITLE_VERBS = [
    "Singing", "Falling", "Rising", "Breaking", "Healing", "Fading", "Growing",
    "Waiting", "Searching", "Finding", "Losing", "Returning", "Departing",
    "Dancing", "Weaving", "Forging", "Shattering", "Binding", "Unraveling",
]


def pick_char(exclude=None):
    """Pick a random character."""
    c = random.choice(characters_data)
    if exclude and c["id"] == exclude:
        c = random.choice(characters_data)
    return c

def pick_place(exclude=None):
    """Pick a random place."""
    p = random.choice(places_data)
    if exclude and p["id"] == exclude:
        p = random.choice(places_data)
    return p

def make_line(character_id, place_id, dialogue, stage_directions=""):
    """Create a line object."""
    return {
        "character": character_id,
        "place": place_id,
        "dialogue": dialogue,
        "stage_directions": stage_directions,
    }

def make_narrative_lines(count, char_id, place_id):
    """Generate narrative lines for a segment."""
    lines = []
    char_name = next((c["name"] for c in characters_data if c["id"] == char_id), char_id)
    place_name = next((p["name"] for p in places_data if p["id"] == place_id), place_id)
    
    for _ in range(count):
        template = random.choice(NARRATIVE_TEMPLATES)
        dialogue = template.format(place_name, char_name)
        stage = random.choice(STAGE_TEMPLATES).format(char_name) if random.random() > 0.5 else ""
        # Use narrator for narrative description lines
        lines.append(make_line("char_narrator", place_id, dialogue, stage))
    
    # Add one spoken line from the character
    voice_lines = CHAR_VOICES.get(char_id, ["I see.", "Interesting.", "We should move."])
    spoken = random.choice(voice_lines)
    stage = random.choice(STAGE_TEMPLATES).format(char_name) if random.random() > 0.3 else ""
    lines.append(make_line(char_id, place_id, spoken, stage))
    
    return lines

def make_decision(char_id, place_id, subplot_id):
    """Generate a decision block."""
    char_name = next((c["name"] for c in characters_data if c["id"] == char_id), "Someone")
    
    prompt_line = make_line(
        char_id, place_id,
        random.choice(DECISION_PROMPTS),
        random.choice(STAGE_TEMPLATES).format(char_name)
    )
    
    # Pick 3 unique choices
    chosen = random.sample(CHOICE_TEMPLATES, 3)
    
    # Ensure one easy, one medium, one hard
    difficulties = [c[1] for c in chosen]
    if "easy" not in difficulties:
        chosen[0] = (chosen[0][0], "easy")
    if "medium" not in difficulties:
        chosen[1] = (chosen[1][0], "medium")
    if "hard" not in difficulties:
        chosen[2] = (chosen[2][0], "hard")
    
    choices = []
    for desc_template, diff in chosen:
        desc = desc_template.replace("{{char}}", char_name)
        
        pass_dialogue = random.choice(PASS_LINES).format(char_name)
        fail_dialogue = random.choice(FAIL_LINES).format(char_name)
        
        choices.append({
            "description": desc,
            "difficulty": diff,
            "subplot": subplot_id,
            "pass_outcome": {
                "line": make_line(char_id, place_id, pass_dialogue),
                "subplot": subplot_id,
                "delta": random.choice([1, 2]),
            },
            "fail_outcome": {
                "line": make_line(char_id, place_id, fail_dialogue),
                "subplot": subplot_id,
                "delta": random.choice([-2, -1]),
            },
        })
    
    return {
        "line": prompt_line,
        "choices": choices,
    }

def make_act(act_num, tag1, tag2, subplot_id):
    """Generate one act with 2 tags in segments format."""
    char = pick_char()
    place = pick_place()
    
    act_id = f"act_{act_num:03d}"
    
    # Title
    noun = random.choice(TITLE_NOUNS)
    verb = random.choice(TITLE_VERBS)
    templates = [f"The {noun} {verb}", f"{verb} at the {noun}", f"{char['name']} and the {noun}", f"The {noun} of {place['name']}"]
    title = random.choice(templates)
    
    segments = [
        {"type": "narrative", "lines": make_narrative_lines(random.randint(2, 3), char["id"], place["id"])},
        {"type": "tag", "tag": tag1},
        {"type": "narrative", "lines": make_narrative_lines(random.randint(2, 3), pick_char(char["id"])["id"], place["id"])},
        {"type": "tag", "tag": tag2},
        {"type": "narrative", "lines": make_narrative_lines(random.randint(2, 3), pick_char(char["id"])["id"], pick_place(place["id"])["id"])},
    ]
    
    decision_char = pick_char()
    decision_place = pick_place()
    decision = make_decision(decision_char["id"], decision_place["id"], subplot_id)
    
    return {
        "id": act_id,
        "title": title,
        "segments": segments,
        "decision": decision,
    }

def make_episode(ep_num, tag_assignment, subplot_id):
    """Generate one complete episode."""
    ep_id = f"ep_{ep_num:03d}"
    
    # Title
    t1 = random.choice(TITLE_TEMPLATES)
    noun1 = random.choice(TITLE_NOUNS)
    noun2 = random.choice(TITLE_NOUNS)
    title = t1.format(noun1, noun2)
    
    acts = []
    for i, (tag1, tag2) in enumerate(tag_assignment):
        acts.append(make_act(i + 1, tag1, tag2, subplot_id))
    
    return {
        "id": ep_id,
        "title": title,
        "acts": acts,
    }

def get_tag_usage():
    """Count how many times each tag is used."""
    usage = {t["id"]: 0 for t in tags_data}
    for ep in all_episodes:
        for act in ep.get("acts", []):
            if "tag" in act:
                tag = act["tag"]
                if tag in usage:
                    usage[tag] += 1
            for seg in act.get("segments", []):
                if isinstance(seg, dict) and seg.get("type") == "tag":
                    tag = seg.get("tag", "")
                    if tag in usage:
                        usage[tag] += 1
    return usage

def validate_episode(ep):
    """Quick validation."""
    errors = []
    if len(ep.get("acts", [])) != 4:
        errors.append(f"Expected 4 acts, got {len(ep.get('acts', []))}")
    
    tag_count = 0
    for act in ep.get("acts", []):
        for seg in act.get("segments", []):
            if seg.get("type") == "tag":
                tag_count += 1
        choices = act.get("decision", {}).get("choices", [])
        if len(choices) != 3:
            errors.append(f"Act {act.get('id')} has {len(choices)} choices")
    
    if tag_count != 8:
        errors.append(f"Expected 8 tags, got {tag_count}")
    
    return len(errors) == 0, errors

def main():
    start_num = len(all_episodes) + 1
    target_count = 510
    
    if start_num > target_count:
        print(f"Already have {len(all_episodes)} episodes.")
        return
    
    to_generate = target_count - len(all_episodes)
    print(f"Have {len(all_episodes)} episodes. Generating {to_generate} more...")
    
    usage = get_tag_usage()
    generated = []
    
    for ep_num in range(start_num, target_count + 1):
        ep_id = f"ep_{ep_num:03d}"
        
        # Get 8 least-used tags
        sorted_tags = sorted(usage.items(), key=lambda x: x[1])
        tag_pool = [t[0] for t in sorted_tags[:8]]
        random.shuffle(tag_pool)
        
        tag_assignment = [
            (tag_pool[0], tag_pool[1]),
            (tag_pool[2], tag_pool[3]),
            (tag_pool[4], tag_pool[5]),
            (tag_pool[6], tag_pool[7]),
        ]
        
        # Update usage
        for t in tag_pool:
            usage[t] += 1
        
        subplot_id = random.choice(VALID_SUBPLOT_IDS)
        
        ep = make_episode(ep_num, tag_assignment, subplot_id)
        
        is_valid, errors = validate_episode(ep)
        if is_valid:
            all_episodes.append(ep)
            generated.append(ep)
            if len(generated) % 10 == 0:
                print(f"  Generated {len(generated)}/170... ({ep_id})")
        else:
            print(f"  Validation error for {ep_id}: {errors}")
    
    # Save
    with open(EPISODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_episodes, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone! Generated {len(generated)} episodes. Total: {len(all_episodes)}")

if __name__ == "__main__":
    main()
