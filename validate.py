#!/usr/bin/env python3
"""
Validation script for the Thai RPG CMS data.
Checks all relations between tables.
"""

import json
import sys


def load_data():
    with open('public/tags.json', 'r', encoding='utf-8') as f:
        tags = json.load(f)
    with open('public/vocab_items.json', 'r', encoding='utf-8') as f:
        vocab_items = json.load(f)
    with open('public/characters.json', 'r', encoding='utf-8') as f:
        characters = json.load(f)
    with open('public/places.json', 'r', encoding='utf-8') as f:
        places = json.load(f)
    with open('public/subplots.json', 'r', encoding='utf-8') as f:
        subplots = json.load(f)
    try:
        with open('public/episodes.json', 'r', encoding='utf-8') as f:
            episodes = json.load(f)
    except FileNotFoundError:
        episodes = []
    return tags, vocab_items, characters, places, subplots, episodes


def validate():
    tags, vocab_items, characters, places, subplots, episodes = load_data()
    errors = []
    warnings = []

    # Build lookup sets
    tag_ids = set(t['id'] for t in tags)
    vocab_ids = set(v['id'] for v in vocab_items)
    char_ids = set(c['id'] for c in characters)
    place_ids = set(p['id'] for p in places)
    subplot_ids = set(s['id'] for s in subplots)
    episode_ids = set(e['id'] for e in episodes)

    # === TAGS ↔ VOCAB_ITEMS ===
    print("=== Checking tags ↔ vocab_items ===")
    for tag in tags:
        num_items = len(tag['vocab_item_ids'])
        if num_items < 5:
            errors.append(f"Tag '{tag['id']}' ({tag['name']}) has only {num_items} vocab items (min: 5)")
        elif num_items > 10:
            errors.append(f"Tag '{tag['id']}' ({tag['name']}) has {num_items} vocab items (max: 10)")

    for vocab in vocab_items:
        num_tags = len(vocab['tag_ids'])
        if num_tags < 5:
            errors.append(f"Vocab item '{vocab['id']}' has only {num_tags} tags (min: 5)")
        elif num_tags > 10:
            errors.append(f"Vocab item '{vocab['id']}' has {num_tags} tags (max: 10)")

    for tag in tags:
        if len(tag['vocab_item_ids']) == 0:
            errors.append(f"Tag '{tag['id']}' is orphaned (no vocab items)")

    for vocab in vocab_items:
        if len(vocab['tag_ids']) == 0:
            errors.append(f"Vocab item '{vocab['id']}' is orphaned (no tags)")

    broken_refs = 0
    for v in vocab_items:
        for tid in v['tag_ids']:
            if tid not in tag_ids:
                errors.append(f"Vocab item '{v['id']}' references non-existent tag '{tid}'")
                broken_refs += 1
    for t in tags:
        for vid in t['vocab_item_ids']:
            if vid not in vocab_ids:
                errors.append(f"Tag '{t['id']}' references non-existent vocab item '{vid}'")
                broken_refs += 1

    # Bidirectional consistency
    for t in tags:
        for vid in t['vocab_item_ids']:
            v = next((v for v in vocab_items if v['id'] == vid), None)
            if v and t['id'] not in v['tag_ids']:
                errors.append(f"Bidirectional: tag '{t['id']}' lists vocab '{vid}', but vocab doesn't list tag")
    for v in vocab_items:
        for tid in v['tag_ids']:
            t = next((t for t in tags if t['id'] == tid), None)
            if t and v['id'] not in t['vocab_item_ids']:
                errors.append(f"Bidirectional: vocab '{v['id']}' lists tag '{tid}', but tag doesn't list vocab")

    # === EPISODES ===
    print("=== Checking episodes ===")
    for ep in episodes:
        if 'title' not in ep:
            errors.append(f"Episode '{ep['id']}' missing title")
        if 'acts' not in ep or not isinstance(ep['acts'], list):
            errors.append(f"Episode '{ep['id']}' missing or invalid acts")
            continue

        for act in ep['acts']:
            act_id = act.get('id', '?')

            # Check lines_before
            for line in act.get('lines_before', []):
                if line.get('character') not in char_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' lines_before references non-existent character '{line.get('character')}'")
                if line.get('place') not in place_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' lines_before references non-existent place '{line.get('place')}'")

            # Check tag reference
            if act.get('tag') and act['tag'] not in tag_ids:
                errors.append(f"Episode '{ep['id']}' act '{act_id}' references non-existent tag '{act['tag']}'")

            # Check lines_after
            for line in act.get('lines_after', []):
                if line.get('character') not in char_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' lines_after references non-existent character '{line.get('character')}'")
                if line.get('place') not in place_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' lines_after references non-existent place '{line.get('place')}'")

            # Check decision
            decision = act.get('decision', {})
            dec_line = decision.get('line', {})
            if dec_line.get('character') not in char_ids:
                errors.append(f"Episode '{ep['id']}' act '{act_id}' decision line references non-existent character '{dec_line.get('character')}'")
            if dec_line.get('place') not in place_ids:
                errors.append(f"Episode '{ep['id']}' act '{act_id}' decision line references non-existent place '{dec_line.get('place')}'")

            choices = decision.get('choices', [])
            if len(choices) != 3:
                warnings.append(f"Episode '{ep['id']}' act '{act_id}' has {len(choices)} choices (expected 3)")

            for choice in choices:
                # Check subplot references
                if choice.get('subplot') not in subplot_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' choice references non-existent subplot '{choice.get('subplot')}'")

                # Check pass outcome
                pass_out = choice.get('pass_outcome', {})
                pass_line = pass_out.get('line', {})
                if pass_line.get('character') not in char_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' pass_outcome references non-existent character '{pass_line.get('character')}'")
                if pass_line.get('place') not in place_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' pass_outcome references non-existent place '{pass_line.get('place')}'")
                if pass_out.get('subplot') not in subplot_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' pass_outcome references non-existent subplot '{pass_out.get('subplot')}'")

                # Check fail outcome
                fail_out = choice.get('fail_outcome', {})
                fail_line = fail_out.get('line', {})
                if fail_line.get('character') not in char_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' fail_outcome references non-existent character '{fail_line.get('character')}'")
                if fail_line.get('place') not in place_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' fail_outcome references non-existent place '{fail_line.get('place')}'")
                if fail_out.get('subplot') not in subplot_ids:
                    errors.append(f"Episode '{ep['id']}' act '{act_id}' fail_outcome references non-existent subplot '{fail_out.get('subplot')}'")

    # === CHARACTERS, PLACES, SUBPLOTS basic checks ===
    print("=== Checking characters, places, subplots ===")
    for c in characters:
        if not c.get('name'):
            errors.append(f"Character '{c['id']}' missing name")
        if not c.get('description'):
            errors.append(f"Character '{c['id']}' missing description")
    for p in places:
        if not p.get('name'):
            errors.append(f"Place '{p['id']}' missing name")
        if not p.get('description'):
            errors.append(f"Place '{p['id']}' missing description")
    for s in subplots:
        if not s.get('name'):
            errors.append(f"Subplot '{s['id']}' missing name")

    # Summary
    print(f"\n=== Validation Results ===")
    print(f"Tags: {len(tags)}, Vocab items: {len(vocab_items)}")
    print(f"Characters: {len(characters)}, Places: {len(places)}")
    print(f"Subplots: {len(subplots)}, Episodes: {len(episodes)}")
    print(f"Errors: {len(errors)}, Warnings: {len(warnings)}")

    if errors:
        print(f"\n=== Errors ===")
        for e in errors:
            print(f"  [FAIL] {e}")
    if warnings:
        print(f"\n=== Warnings ===")
        for w in warnings:
            print(f"  [WARN] {w}")

    if not errors:
        print("\nAll validations passed!")
        return 0
    else:
        print(f"\n{len(errors)} validation errors found.")
        return 1


if __name__ == '__main__':
    sys.exit(validate())
