#!/usr/bin/env python3
"""
Validation script for the Thai RPG CMS data.
Checks:
1. No orphaned items (all tags have items, all items have tags)
2. Referential integrity (all pointers point to existing items)
3. Each tag has 5-10 vocab items
4. Each vocab item has 5-10 tags
"""

import json
import sys


def load_data():
    with open('public/tags.json', 'r', encoding='utf-8') as f:
        tags = json.load(f)
    with open('public/vocab_items.json', 'r', encoding='utf-8') as f:
        vocab_items = json.load(f)
    return tags, vocab_items


def validate():
    tags, vocab_items = load_data()
    errors = []
    warnings = []

    # Build lookup sets
    tag_ids = set(t['id'] for t in tags)
    vocab_ids = set(v['id'] for v in vocab_items)

    # 1. Check tag constraints: 5-10 vocab items per tag
    for tag in tags:
        num_items = len(tag['vocab_item_ids'])
        if num_items < 5:
            errors.append(f"Tag '{tag['id']}' ({tag['name']}) has only {num_items} vocab items (min: 5)")
        elif num_items > 10:
            errors.append(f"Tag '{tag['id']}' ({tag['name']}) has {num_items} vocab items (max: 10)")

    # 2. Check vocab item constraints: 5-10 tags per item
    for vocab in vocab_items:
        num_tags = len(vocab['tag_ids'])
        if num_tags < 5:
            errors.append(f"Vocab item '{vocab['id']}' has only {num_tags} tags (min: 5)")
        elif num_tags > 10:
            errors.append(f"Vocab item '{vocab['id']}' has {num_tags} tags (max: 10)")

    # 3. Check for orphaned tags (tags with no items)
    for tag in tags:
        if len(tag['vocab_item_ids']) == 0:
            errors.append(f"Tag '{tag['id']}' is orphaned (no vocab items)")

    # 4. Check for orphaned vocab items (items with no tags)
    for vocab in vocab_items:
        if len(vocab['tag_ids']) == 0:
            errors.append(f"Vocab item '{vocab['id']}' is orphaned (no tags)")

    # 5. Referential integrity: tags -> vocab items
    for tag in tags:
        for vid in tag['vocab_item_ids']:
            if vid not in vocab_ids:
                errors.append(f"Tag '{tag['id']}' references non-existent vocab item '{vid}'")

    # 6. Referential integrity: vocab items -> tags
    for vocab in vocab_items:
        for tid in vocab['tag_ids']:
            if tid not in tag_ids:
                errors.append(f"Vocab item '{vocab['id']}' references non-existent tag '{tid}'")

    # 7. Check bidirectional consistency (many-to-many integrity)
    for tag in tags:
        for vid in tag['vocab_item_ids']:
            vocab = next((v for v in vocab_items if v['id'] == vid), None)
            if vocab and tag['id'] not in vocab['tag_ids']:
                errors.append(f"Bidirectional inconsistency: tag '{tag['id']}' lists vocab '{vid}', but vocab does not list tag")

    for vocab in vocab_items:
        for tid in vocab['tag_ids']:
            tag = next((t for t in tags if t['id'] == tid), None)
            if tag and vocab['id'] not in tag['vocab_item_ids']:
                errors.append(f"Bidirectional inconsistency: vocab '{vocab['id']}' lists tag '{tid}', but tag does not list vocab")

    # Summary
    print(f"=== Validation Results ===")
    print(f"Tags: {len(tags)}")
    print(f"Vocab items: {len(vocab_items)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

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
