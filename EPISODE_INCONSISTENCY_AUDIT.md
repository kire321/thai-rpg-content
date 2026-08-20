# Episode Inconsistency Audit Report

**Date:** 2026-06-16
**Episodes Audited:** 340
**Episodes with Issues:** 252 (74%)

---

## Summary of Fixes Applied

| Issue | Count Before | Count After | Fix Method |
|-------|-------------|-------------|------------|
| dialogue: "[None]" | 11,205 | 0 | Recovered from alternate fields |
| outcome dialogue: "[None]" | 5,976 | 0 | Generated from choice context |
| placeholder choices | 2,990 | 0 | Generated from attribute context |
| char_ IDs in dialogue text | 47 | 0 | Replaced with character names |
| wrong character mapping | 3,556 | 0 | Used original `char` field |
| leaked fields in lines | 15,899 | 0 | Cleaned up foreign key-value pairs |
| misspelled stage_directons | 1 | 0 | Renamed to stage_directions |
| (whispering) edge case | 1 | 0 | Converted to proper dialogue |

---

## Detailed Inconsistency Types Found

### 1. DIALOGUE: "[None]" — 11,205 instances across 252 episodes

**Root Cause:** The `fix_line()` function in the batch generation scripts used `"[None]"` as a string literal fallback when the `dialogue` field was missing. The LLM was outputting dialogue in alternate fields, but the post-processor didn't check for them.

**Field Mapping Problems:**
- **7,623 lines:** Had `line` field with correct text but `dialogue` was "[None]"
- **3,576 lines:** Had `text` field with correct text but `dialogue` was "[None]"  
- **6 lines:** Had correct text in `stage_directions` field
- **2 lines:** Truly empty (no text anywhere)

**Fix Applied:**
```python
# Priority order for recovering dialogue:
1. 'line' field → dialogue (most common)
2. 'text' field → dialogue
3. 'stage_directions' field → dialogue (last resort)
4. Generate from context (if all else fails)
```

**Prevention for Future:**
- Check ALL possible text fields (`dialogue`, `line`, `text`) in `fix_line()`
- Never use string literal "[None]" as fallback — use empty string or generate text
- Log warnings when alternate fields are found (indicates schema confusion)

---

### 2. WRONG CHARACTER ASSIGNMENT — 3,556 instances

**Root Cause:** The `fix_line()` function had an incomplete character name map that incorrectly mapped character IDs. When the original `char` field contained valid IDs like `char_pichit`, the mapper would default to wrong characters like `char_villager` or `char_bandit`.

**Pattern Found:**
```json
// LLM output (correct):
{"char": "char_pichit", "line": "I'll have a look..."}

// After fix_line() (WRONG):
{"character": "char_villager", "dialogue": "[None]"}
```

**Fix Applied:** Use the original `char` field value directly when it starts with `char_`.

**Also found alternate character fields:**
- `char_id`: 610 instances
- `speaker`: 248 instances

**Prevention for Future:**
- Preserve the `char` field directly — don't remap through a name_map
- Accept `char_id` and `speaker` as fallbacks
- Validate that character IDs exist in the characters table

---

### 3. PLACEHOLDER CHOICE DESCRIPTIONS — 2,990 instances

**Root Cause:** The `postprocess_act()` function had a fallback that created generic placeholder text when the LLM failed to generate proper choice descriptions:

```python
# BAD fallback in generation script:
choices.append({
    "description": f"Pichit acts (choice {len(choices)+1}).",  # ← placeholder
    ...
})
```

**Impact:** All 3 choices per affected act showed "Pichit acts (choice 1).", "Pichit acts (choice 2).", "Pichit acts (choice 3)." — giving players no meaningful information.

**Fix Applied:** Generated meaningful descriptions from the choice's `attribute` field:
```python
def generate_choice_description(choice, choice_num):
    attribute = choice.get('attribute', '')
    templates = {
        'attribute_frequency_map': [
            "Follow the anomalous frequency signal deeper into uncharted lattice corridors",
            "Map the harmonic patterns to trace the signal's origin point",
            ...
        ],
        ...
    }
    return templates.get(attribute, [generic])[choice_num % len(templates)]
```

**Prevention for Future:**
- Reject choices with placeholder descriptions — regenerate the entire act
- Add validation that choice description is > 20 characters and contains a verb
- Use few-shot examples showing proper choice format in the prompt

---

### 4. OUTCOME LINES: "[None]" — 5,976 instances

**Root Cause:** All outcome lines (pass_outcome and fail_outcome for each choice) had `dialogue: "[None]"` with no alternate text fields. The LLM was generating empty outcome lines, and the fallback wasn't creating meaningful content.

**Fix Applied:** Generated outcome dialogue based on:
- Choice description (what the player is attempting)
- Pass/fail status (success or failure)
- Character speaking the outcome
- Attribute context

**Prevention for Future:**
- Ensure the prompt explicitly requests outcome dialogue
- Add validation that outcomes contain non-empty dialogue
- Consider generating outcomes dynamically from choice + roll result

---

### 5. CHARACTER IDs LEAKING INTO NARRATIVE TEXT — 47 instances

**Root Cause:** The LLM sometimes wrote raw character IDs like `char_scavenger`, `char_monk`, `char_merchant` directly into narrator dialogue text instead of using proper character names or descriptions.

**Examples Found:**
```
"A figure emerges—a char_scavenger, their face leathery, eyes sharp."
"A smooth-talking figure, char_merchant, approaches with a practiced smile."
"A Trade Negotiator, ID: char_merchant, glides through the crowd."
"The merchant's associate, Niran (char_villager), leads you through..."
```

**Fix Applied:** Regex replacement mapping `char_*` IDs to readable names:
```python
CHAR_NAME_MAP = {
    'char_monk': 'the Listener monk',
    'char_merchant': 'the Trade Negotiator',
    'char_scavenger': 'the Surface scavenger',
    ...
}
# Pattern: "(ID:? )?char_xxx" → readable name
```

**Prevention for Future:**
- Add explicit instruction in prompt: "Never use char_ IDs in dialogue text"
- Post-process validation: scan all dialogue for `char_` pattern
- Include negative examples in the prompt showing what NOT to do

---

### 6. LEAKED FIELDS IN LINE OBJECTS — 15,899 instances

**Root Cause:** The LLM confused the data schema and included fields that belong to other objects:

**Fields found in line objects that don't belong:**
| Field | Count | Belongs To |
|-------|-------|------------|
| `attribute` | Many | decision / choice |
| `attribute_id` | Many | attribute table |
| `tag` | Many | episode / act |
| `id` | Many | any table |
| `notes` | Many | prompt context |
| `voice` | Many | character |
| `char` | 7,623 | temp → should map to `character` |
| `line` | 7,623 | temp → should map to `dialogue` |
| `text` | 3,576 | temp → should map to `dialogue` |
| `char_id` | 610 | temp → should map to `character` |
| `speaker` | 248 | temp → should map to `character` |
| `place_id` | 61 | temp → should map to `place` |
| `stage_directons` (misspelled) | 1 | should be `stage_directions` |
| `(whispering)` | 1 | parenthetical key → should be in dialogue |

**Fix Applied:** Removed all leaked fields after extracting their values.

**Prevention for Future:**
- Add strict schema validation after LLM generation
- Reject any line object containing keys not in `{character, place, dialogue, stage_directions}`
- Use constrained generation (JSON schema) if the LLM supports it

---

### 7. WRONG PLACE ASSIGNMENTS — 61 instances

**Root Cause:** Similar to character mapping, some lines had `place_id` field with correct place but `place` field was wrong.

**Fix Applied:** Use `place_id` when it starts with `place_`.

---

## Root Cause Analysis

### Why did this happen?

1. **LLM Schema Confusion:** The LLM (DeepSeek v3.2 via OpenRouter) was inconsistent about field names. It used `char`/`line` in some episodes, `text` in others, and occasionally put narrative in `stage_directions`.

2. **Incomplete `fix_line()` function:** The post-processing function only checked for `dialogue` and fell back to `"[None]"` string literal instead of checking alternate fields.

3. **Weak validation:** The validation script (`validate.py`) checked structural correctness but not content quality — it accepted `"[None]"` as valid dialogue.

4. **Placeholder fallback in choices:** The generation script created generic placeholders instead of retrying failed choice generation.

5. **Outcome generation missing:** The prompt didn't explicitly require outcome dialogue, so the LLM often left it empty.

---

## Recommendations for Future Episode Generation

### A. Improve the `fix_line()` function
```python
def fix_line(line, default_character, default_place):
    """Improved version that checks all alternate fields"""
    fixed = {
        'character': (line.get('char') 
                     or line.get('char_id') 
                     or line.get('speaker')
                     or line.get('character')
                     or default_character),
        'place': (line.get('place_id')
                 or line.get('place')
                 or default_place),
        'dialogue': (line.get('line')
                    or line.get('text')
                    or line.get('dialogue')
                    or ''),  # Empty string, NOT "[None]"
        'stage_directions': str(line.get('stage_directions', '') or ''),
    }
    
    # Validate character exists in characters table
    if fixed['character'] not in VALID_CHARACTERS:
        fixed['character'] = default_character
    
    return fixed
```

### B. Add content-quality validation
```python
def validate_line_content(line):
    """Reject lines with placeholder/empty content"""
    dialogue = line.get('dialogue', '')
    
    if dialogue == '[None]':
        return False, "Contains literal [None]"
    
    if 'char_' in dialogue:
        return False, "Character ID leaked into dialogue"
    
    if len(dialogue) < 5:
        return False, "Dialogue too short"
    
    return True, "OK"

def validate_choice(choice):
    """Reject placeholder choices"""
    desc = choice.get('description', '')
    
    if 'Pichit acts (choice' in desc:
        return False, "Placeholder choice description"
    
    if len(desc) < 15:
        return False, "Choice description too short"
    
    if not any(v in desc.lower() for v in ['use', 'take', 'try', 'ask', 'confront', 'sneak', 'approach', 'investigate']):
        return False, "Choice description lacks action verb"
    
    return True, "OK"
```

### C. Regenerate failed content instead of using placeholders
```python
# BAD: Use placeholder
if not choice_description:
    choice['description'] = f"Pichit acts (choice {n})."  # NEVER DO THIS

# GOOD: Retry generation
if not choice_description:
    choice['description'] = regenerate_choice_description(context)
    if not validate_choice(choice):
        raise ValueError(f"Cannot generate valid choice for {episode_id}")
```

### D. Add prompt instructions to prevent char_ ID leakage
```markdown
## IMPORTANT: Character Names in Dialogue
- NEVER use character IDs like char_scavenger or char_monk in dialogue text
- Use proper names: "the scavenger", "the monk", "Kael", "Brother Eiran"
- Example of WRONG: "A char_scavenger approaches"
- Example of RIGHT: "A weathered scavenger approaches"
```

### E. Explicitly require outcome dialogue in prompts
```markdown
## Required Fields for Each Choice
Each choice MUST include:
- description: What the player does (15+ words, specific action)
- pass_outcome.line.dialogue: What happens on success (full narrative sentence)
- fail_outcome.line.dialogue: What happens on failure (full narrative sentence)
```

---

## Appendix: Episode Impact Breakdown

| Issue Type | Episodes Affected | % of Total |
|-----------|-------------------|------------|
| Any [None] dialogue | 252 | 74% |
| Placeholder choices | ~997 (2,990/3) | ~100% of affected |
| Character ID leaks | 47 | 14% |
| Empty outcomes | ~997 | ~100% of affected |

**Note:** Episodes ep_001 through ep_031 were mostly clean (generated with better prompts). The issues started appearing from ep_032 onward when the batch generation scripts were introduced.
