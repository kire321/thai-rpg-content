#!/usr/bin/env python3
"""Validate the Chantara CMS catalog and both act formats.

The validator is intentionally data-driven: legacy acts keep their one tag,
while segmented acts may contain any number of narrative/tag segments.  The
staging contract adds the stricter two-tags-per-act rule only to ep_341 onward.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
LINE_KEYS = {"character", "place", "dialogue", "stage_directions"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}
CHARACTER_ID_RE = re.compile(r"\bchar_[a-z0-9_]+\b")


def load_json(filename: str):
    with (PUBLIC / filename).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_data():
    return (
        load_json("tags.json"),
        load_json("vocab_items.json"),
        load_json("characters.json"),
        load_json("places.json"),
        load_json("subplots.json"),
        load_json("episodes.json") if (PUBLIC / "episodes.json").exists() else [],
    )


def is_new_episode(episode: dict) -> bool:
    match = re.fullmatch(r"ep_(\d+)", str(episode.get("id", "")))
    return bool(match and int(match.group(1)) >= 341)


def line_error(
    line: object,
    *,
    context: str,
    char_ids: set[str],
    place_ids: set[str],
    errors: list[str],
    quality: bool = True,
):
    if not isinstance(line, dict):
        errors.append(f"{context} is not an object")
        return

    missing = LINE_KEYS - set(line)
    extra = set(line) - LINE_KEYS
    if missing:
        errors.append(f"{context} is missing line fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{context} has unexpected line fields: {', '.join(sorted(extra))}")

    character = line.get("character")
    place = line.get("place")
    if character not in char_ids:
        errors.append(f"{context} references non-existent character '{character}'")
    if place not in place_ids:
        errors.append(f"{context} references non-existent place '{place}'")

    if not isinstance(line.get("dialogue"), str) or not line.get("dialogue", "").strip():
        errors.append(f"{context} has empty dialogue")
    if not isinstance(line.get("stage_directions"), str):
        errors.append(f"{context} stage_directions must be a string")

    if quality:
        dialogue = line.get("dialogue", "")
        if dialogue == "[None]" or "[None]" in dialogue:
            errors.append(f"{context} contains placeholder dialogue '[None]'")
        if CHARACTER_ID_RE.search(dialogue):
            errors.append(f"{context} leaks a character ID into dialogue")


def act_segments(act: dict, *, context: str, errors: list[str]):
    """Return (segments, format_name), translating a legacy act for checks."""
    if isinstance(act.get("segments"), list):
        return act["segments"], "segments"
    if isinstance(act.get("steps"), list):
        return act["steps"], "steps"
    if "lines_before" in act or "lines_after" in act or "tag" in act:
        return [
            {"type": "narrative", "lines": act.get("lines_before", [])},
            {"type": "tag", "tag": act.get("tag")},
            {"type": "narrative", "lines": act.get("lines_after", [])},
        ], "legacy"
    errors.append(f"{context} has neither segments nor legacy narrative fields")
    return [], "unknown"


def validate():
    tags, vocab_items, characters, places, subplots, episodes = load_data()
    errors: list[str] = []
    warnings: list[str] = []

    def ids(items: list[dict], label: str) -> set[str]:
        values = [item.get("id") for item in items]
        counts = Counter(values)
        for value, count in counts.items():
            if not value or count > 1:
                errors.append(f"{label} has duplicate or empty id '{value}'")
        return {value for value in values if isinstance(value, str)}

    tag_ids = ids(tags, "tags")
    vocab_ids = ids(vocab_items, "vocab_items")
    char_ids = ids(characters, "characters")
    place_ids = ids(places, "places")
    subplot_ids = ids(subplots, "subplots")
    episode_ids = ids(episodes, "episodes")

    print("=== Checking tags ↔ vocab_items ===")
    for tag in tags:
        vocab_refs = tag.get("vocab_item_ids", [])
        if not isinstance(vocab_refs, list) or not 5 <= len(vocab_refs) <= 10:
            errors.append(f"Tag '{tag.get('id')}' must contain 5-10 vocab items")
        for vocab_id in vocab_refs if isinstance(vocab_refs, list) else []:
            if vocab_id not in vocab_ids:
                errors.append(f"Tag '{tag.get('id')}' references non-existent vocab '{vocab_id}'")

    for vocab in vocab_items:
        tag_refs = vocab.get("tag_ids", [])
        if not isinstance(tag_refs, list) or not 5 <= len(tag_refs) <= 10:
            errors.append(f"Vocab item '{vocab.get('id')}' must contain 5-10 tags")
        for tag_id in tag_refs if isinstance(tag_refs, list) else []:
            if tag_id not in tag_ids:
                errors.append(f"Vocab item '{vocab.get('id')}' references non-existent tag '{tag_id}'")

    tag_map = {tag.get("id"): tag for tag in tags}
    vocab_map = {vocab.get("id"): vocab for vocab in vocab_items}
    for tag in tags:
        for vocab_id in tag.get("vocab_item_ids", []):
            if vocab_id in vocab_map and tag.get("id") not in vocab_map[vocab_id].get("tag_ids", []):
                errors.append(f"Bidirectional mismatch: {tag.get('id')} ↔ {vocab_id}")
    for vocab in vocab_items:
        for tag_id in vocab.get("tag_ids", []):
            if tag_id in tag_map and vocab.get("id") not in tag_map[tag_id].get("vocab_item_ids", []):
                errors.append(f"Bidirectional mismatch: {vocab.get('id')} ↔ {tag_id}")

    print("=== Checking episodes ===")
    tag_usage: Counter[str] = Counter()
    new_tag_usage: Counter[str] = Counter()
    for episode in episodes:
        episode_id = episode.get("id", "?")
        context = f"Episode '{episode_id}'"
        if not episode.get("title"):
            errors.append(f"{context} missing title")
        acts = episode.get("acts")
        if not isinstance(acts, list) or len(acts) != 4:
            errors.append(f"{context} must have exactly 4 acts")
            continue

        for act_index, act in enumerate(acts):
            act_context = f"{context} act '{act.get('id', act_index + 1)}'"
            segments, format_name = act_segments(act, context=act_context, errors=errors)
            tags_in_act: list[str] = []
            previous_type = None
            for segment_index, segment in enumerate(segments):
                segment_context = f"{act_context} segment {segment_index + 1}"
                if not isinstance(segment, dict):
                    errors.append(f"{segment_context} is not an object")
                    continue
                segment_type = segment.get("type")
                if segment_type == "narrative":
                    lines = segment.get("lines")
                    if not isinstance(lines, list) or not lines:
                        errors.append(f"{segment_context} narrative segment must contain lines")
                    for line_index, line in enumerate(lines if isinstance(lines, list) else []):
                        line_error(
                            line,
                            context=f"{segment_context} line {line_index + 1}",
                            char_ids=char_ids,
                            place_ids=place_ids,
                            errors=errors,
                            quality=is_new_episode(episode),
                        )
                elif segment_type == "tag":
                    tag_id = segment.get("tag")
                    if tag_id not in tag_ids:
                        errors.append(f"{segment_context} references non-existent tag '{tag_id}'")
                    else:
                        tags_in_act.append(tag_id)
                        tag_usage[tag_id] += 1
                        if is_new_episode(episode):
                            new_tag_usage[tag_id] += 1
                    if previous_type == "tag":
                        errors.append(f"{segment_context} has adjacent tag segments")
                else:
                    errors.append(f"{segment_context} has unknown type '{segment_type}'")
                previous_type = segment_type

            if format_name in {"segments", "steps"}:
                if not segments or segments[0].get("type") != "narrative":
                    errors.append(f"{act_context} must start with a narrative segment")
                if not segments or segments[-1].get("type") != "narrative":
                    errors.append(f"{act_context} must end with a narrative segment")
            if is_new_episode(episode) and len(tags_in_act) != 2:
                errors.append(f"{act_context} must have exactly 2 tag segments, found {len(tags_in_act)}")
            if len(tags_in_act) != len(set(tags_in_act)):
                errors.append(f"{act_context} repeats a tag within the act")

            decision = act.get("decision")
            if not isinstance(decision, dict):
                errors.append(f"{act_context} is missing decision/options")
                continue
            line_error(
                decision.get("line"),
                context=f"{act_context} decision line",
                char_ids=char_ids,
                place_ids=place_ids,
                errors=errors,
                quality=is_new_episode(episode),
            )
            choices = decision.get("choices")
            if not isinstance(choices, list) or len(choices) != 3:
                errors.append(f"{act_context} must have exactly 3 choices")
                choices = choices if isinstance(choices, list) else []
            difficulties = [choice.get("difficulty") for choice in choices if isinstance(choice, dict)]
            if is_new_episode(episode) and set(difficulties) != VALID_DIFFICULTIES:
                errors.append(f"{act_context} choices must include easy, medium, and hard difficulties")

            for choice_index, choice in enumerate(choices):
                choice_context = f"{act_context} choice {choice_index + 1}"
                if not isinstance(choice, dict):
                    errors.append(f"{choice_context} is not an object")
                    continue
                description = choice.get("description")
                if is_new_episode(episode) and (not isinstance(description, str) or len(description.strip()) < 15):
                    errors.append(f"{choice_context} has an unusable description")
                if is_new_episode(episode) and "choice" in str(description).lower() and "acts" in str(description).lower():
                    errors.append(f"{choice_context} contains a placeholder description")
                subplot = choice.get("subplot")
                if subplot not in subplot_ids:
                    errors.append(f"{choice_context} references non-existent subplot '{subplot}'")
                for outcome_key in ("pass_outcome", "fail_outcome"):
                    outcome = choice.get(outcome_key)
                    outcome_context = f"{choice_context} {outcome_key}"
                    if not isinstance(outcome, dict):
                        errors.append(f"{outcome_context} is missing")
                        continue
                    if outcome.get("subplot") not in subplot_ids:
                        errors.append(f"{outcome_context} references non-existent subplot '{outcome.get('subplot')}'")
                    if is_new_episode(episode) and outcome.get("subplot") != subplot:
                        errors.append(f"{outcome_context} subplot must match its choice")
                    line_error(
                        outcome.get("line"),
                        context=f"{outcome_context} line",
                        char_ids=char_ids,
                        place_ids=place_ids,
                        errors=errors,
                        quality=is_new_episode(episode),
                    )
                    delta = outcome.get("delta")
                    if is_new_episode(episode) and (not isinstance(delta, (int, float)) or not -2 <= delta <= 2):
                        errors.append(f"{outcome_context} delta must be between -2 and 2")
                    if is_new_episode(episode) and outcome_key == "pass_outcome" and isinstance(delta, (int, float)) and delta <= 0:
                        errors.append(f"{outcome_context} should have a positive delta")
                    if is_new_episode(episode) and outcome_key == "fail_outcome" and isinstance(delta, (int, float)) and delta > 0:
                        errors.append(f"{outcome_context} should not have a positive delta")

    print("=== Checking characters, places, and subplots ===")
    if len(characters) < 30:
        errors.append(f"Expected at least 30 characters after the staging expansion, found {len(characters)}")
    if len(places) < 30:
        errors.append(f"Expected at least 30 places after the staging expansion, found {len(places)}")
    for character in characters:
        if not character.get("name") or not character.get("description"):
            errors.append(f"Character '{character.get('id')}' is missing name or description")
        picture = character.get("picture", "").lstrip("/")
        if picture and not (PUBLIC / picture).exists():
            errors.append(f"Character '{character.get('id')}' picture is missing: {picture}")
    for place in places:
        if not place.get("name") or not place.get("description"):
            errors.append(f"Place '{place.get('id')}' is missing name or description")
        picture = place.get("picture", "").lstrip("/")
        if picture and not (PUBLIC / picture).exists():
            errors.append(f"Place '{place.get('id')}' picture is missing: {picture}")
    for subplot in subplots:
        if not subplot.get("name") or not subplot.get("description"):
            errors.append(f"Subplot '{subplot.get('id')}' is missing name or description")

    if len(episodes) != 510:
        errors.append(f"Expected 510 episodes after the staging expansion, found {len(episodes)}")
    expected_new_ids = {f"ep_{number:03d}" for number in range(341, 511)}
    actual_new_ids = {episode.get("id") for episode in episodes if is_new_episode(episode)}
    missing_new = sorted(expected_new_ids - actual_new_ids)
    if missing_new:
        errors.append(f"Missing new episode IDs: {', '.join(missing_new[:10])}{'...' if len(missing_new) > 10 else ''}")

    missing_tags = sorted(tag_ids - set(tag_usage))
    if missing_tags:
        errors.append(f"Unused tags remain: {', '.join(missing_tags[:10])}{'...' if len(missing_tags) > 10 else ''}")
    if tag_usage:
        spread = max(tag_usage.values()) - min(tag_usage.values())
        if spread > 2:
            errors.append(f"Tag usage is not evenly distributed (range {min(tag_usage.values())}-{max(tag_usage.values())})")

    print("\n=== Validation Results ===")
    print(f"Tags: {len(tags)}, Vocab items: {len(vocab_items)}")
    print(f"Characters: {len(characters)}, Places: {len(places)}")
    print(f"Subplots: {len(subplots)}, Episodes: {len(episodes)}")
    print(f"Tag uses: {sum(tag_usage.values())}; range: {min(tag_usage.values(), default=0)}-{max(tag_usage.values(), default=0)}")
    print(f"New-episode tag uses: {sum(new_tag_usage.values())}")
    print(f"Errors: {len(errors)}, Warnings: {len(warnings)}")

    if errors:
        print("\n=== Errors ===")
        for error in errors:
            print(f"  [FAIL] {error}")
    if warnings:
        print("\n=== Warnings ===")
        for warning in warnings:
            print(f"  [WARN] {warning}")

    if errors:
        print(f"\n{len(errors)} validation errors found.")
        return 1
    print("\nAll validations passed!")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
