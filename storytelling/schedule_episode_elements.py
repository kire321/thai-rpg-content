#!/usr/bin/env python3
"""Episode element scheduler for the canal-side Siam world.

Deals each episode-writing sub-agent a complete package of narrative elements:

  - 8 tags (two per act), distributed evenly across episodes (least-used-first)
  - 4 pairs of conflicting PC priorities (one per act), drawn from the 10
    possible pairings of the PC's 5 attributes, distributed evenly
    - each act's decision is a dilemma between the two priorities
    - EASY and MEDIUM each sacrifice one priority; HARD bypasses the dilemma
  - the recurring cast in shuffled priority order; the top character is the
    episode's foregrounded party member
  - the foregrounded character's 3 associated places, in shuffled priority
    order, with private narrative plans and their associated NPC "extras"
    - consumption rule: on travel use the first unused location; on an NPC
      entrance use the first unused extra

Distribution guarantee: priority is spread EVENLY, not randomly and not by
rotation.  Headline slots (tags, priority pairs, foregrounded character) are
least-used-first with a per-episode hash tiebreak, so every element's share is
flat within +-1 over any batch.  Ordering slots (cast order, place order,
pair/act orientation) use a seeded hash of (episode id, element id), so every
episode gets a distinct permutation with no fixed adjacency — unlike a plain
rotation, where "city" always following "cave" would make travel predictable.

Stdlib only.  Deterministic: same command line -> same output.

Usage:
  python3 storytelling/schedule_episode_elements.py --start 11 --count 30 \
      --out packages.json
  python3 storytelling/schedule_episode_elements.py --selftest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PRIVATE = ROOT / "storytelling" / "private"

EPISODES_PATH = PUBLIC / "episodes.json"
TAGS_PATH = PUBLIC / "tags.json"
VOCAB_PATH = PUBLIC / "vocab_items.json"
ATTRIBUTES_PATH = PUBLIC / "attributes.json"
CHARACTERS_PATH = PUBLIC / "characters.json"
PLACES_PATH = PUBLIC / "places.json"

# ---------------------------------------------------------------------------
# World wiring (derived from storytelling/private/*_private.md dialectic
# assignments).  Each recurring character owns one dialectic and 3 places.
# place_veranda is the hub: present in every episode, never foregrounded.
# ---------------------------------------------------------------------------

CHARACTER_PLACES = {
    "char_phum": ["place_river_post", "place_mirror_mender", "place_salt_store"],
    "char_phra_kam": ["place_ash_urn", "place_donation_mirror", "place_silent_pond"],
    "char_sangwan": ["place_letter_writers_landing", "place_wai_khru_mound", "place_pawnshop"],
    "char_mor_duang": ["place_funeral_parlor", "place_rain_gauge_house", "place_water_blessing_ghat"],
    "char_pornchai": ["place_charcoal_hearth", "place_grammar_mill", "place_rice_ledger"],
    "char_rangsri": ["place_laughing_well", "place_rice_counter", "place_spirit_hall"],
}

# Each place's associated NPC "extras", in consumption order (first unused).
PLACE_EXTRAS = {
    "place_river_post": ["char_delivery_boy"],
    "place_mirror_mender": ["char_mirror_mender"],
    "place_salt_store": ["char_salt_clerk"],
    "place_ash_urn": ["char_urn_keeper"],
    "place_donation_mirror": ["char_mirror_tender"],
    "place_silent_pond": ["char_pond_diver"],
    "place_letter_writers_landing": ["char_boatman"],
    "place_wai_khru_mound": ["char_wai_khru_caretaker"],
    "place_pawnshop": ["char_pawnshop_appraiser"],
    "place_funeral_parlor": ["char_funeral_timekeeper"],
    "place_rain_gauge_house": ["char_rain_gauge_keeper"],
    "place_water_blessing_ghat": ["char_water_blessing_drummer"],
    "place_charcoal_hearth": ["char_fire_stoker"],
    "place_grammar_mill": ["char_type_monitor"],
    "place_rice_ledger": ["char_tax_clerk"],
    "place_laughing_well": ["char_well_keeper"],
    "place_rice_counter": ["char_grain_clerk"],
    "place_spirit_hall": ["char_contract_clerk"],
}

# place_pawnshop has no private plan file; the appraiser's plan covers it.
PLACES_WITHOUT_PRIVATE_PLAN = {"place_pawnshop"}


def stable_int(text: str) -> int:
    """Deterministic 64-bit hash — the repo's standard tiebreaker."""
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")


def _pairings(items):
    """All perfect pairings of an even-length list (deterministic order)."""
    if len(items) < 2:
        yield []
        return
    first = items[0]
    for i in range(1, len(items)):
        pair = (first, items[i])
        for rest in _pairings(items[1:i] + items[i + 1:]):
            yield [pair] + rest


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_plan(entity_id: str) -> str:
    """Return an entity's private narrative plan, or a note if none exists."""
    path = PRIVATE / f"{entity_id}_private.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    if entity_id in PLACES_WITHOUT_PRIVATE_PLAN:
        return ("(no private plan file — the associated NPC's private plan "
                "covers this place)")
    return "(no private plan file)"


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self, data: dict, start_ep: int):
        self.tags = data["tags"]
        self.attributes = data["attributes"]
        self.characters = data["characters"]
        self.places = data["places"]
        self.party_ids = [c["id"] for c in self.characters if c.get("type") == "party"]
        assert sorted(self.party_ids) == sorted(CHARACTER_PLACES), (
            "CHARACTER_PLACES must cover exactly the party members")
        self.place_ids = {p["id"] for p in self.places}
        for pid_list in CHARACTER_PLACES.values():
            for pid in pid_list:
                assert pid in self.place_ids, f"unknown place {pid}"
        for pid, extras in PLACE_EXTRAS.items():
            assert pid in self.place_ids, f"unknown place {pid}"
            for ex in extras:
                assert any(c["id"] == ex for c in self.characters), f"unknown extra {ex}"

        # All C(5,2) = 10 pairings of the PC's priorities.
        self.all_pairs = [
            (a["id"], b["id"])
            for i, a in enumerate(self.attributes)
            for b in self.attributes[i + 1:]
        ]
        # Tag usage seeded from content that already exists.
        self.tag_usage = {t["id"]: 0 for t in self.tags}
        for ep in data.get("episodes", []):
            for act in ep.get("acts", []):
                if "tag" in act and act["tag"] in self.tag_usage:
                    self.tag_usage[act["tag"]] += 1
                for seg in act.get("segments", []):
                    if isinstance(seg, dict) and seg.get("type") == "tag" \
                            and seg.get("tag") in self.tag_usage:
                        self.tag_usage[seg["tag"]] += 1
        self.pair_usage = {p: 0 for p in self.all_pairs}
        self.foreground_usage = {c: 0 for c in self.party_ids}
        self._vocab = {v["id"]: v for v in data["vocab"]}
        self.start_ep = start_ep

    # -- dealing primitives --------------------------------------------------

    def _least_used(self, elements, usage, ep_id, salt):
        """Least-used-first with a per-episode hash tiebreak: even shares,
        unpredictable order, no rotation artifacts."""
        return sorted(elements, key=lambda e: (usage[e], stable_int(f"{ep_id}:{salt}:{e}")))

    def _hash_order(self, elements, ep_id, salt):
        """Full permutation by seeded hash — adjacency changes completely
        from episode to episode."""
        return sorted(elements, key=lambda e: stable_int(f"{ep_id}:{salt}:{e}"))

    # -- per-episode package -------------------------------------------------

    def deal(self, ep_num: int) -> dict:
        ep_id = f"ep_{ep_num:03d}"

        # 8 tags: least-used-first, then hash-shuffle into 4 act pairs.
        # Avoid same-family pairings within an act (tag_198 + tag_202 would
        # force two near-identical anchors into one quiz pair): enumerate all
        # 105 pairings of the 8 and take the first with no same-family pair.
        ordered_tags = self._least_used(
            list(self.tag_usage), self.tag_usage, ep_id, "tags")
        eight = ordered_tags[:8]
        shuffled8 = self._hash_order(eight, ep_id, "tagpairs")
        fam = self._tag_family
        act_tags = None
        for pairing in _pairings(shuffled8):
            if all(fam(a) != fam(b) for a, b in pairing):
                act_tags = pairing
                break
        if act_tags is None:  # 8 tags from one family — take any pairing
            act_tags = [(shuffled8[i], shuffled8[i + 1]) for i in range(0, 8, 2)]
        for t in eight:
            self.tag_usage[t] += 1

        # 4 priority pairs: least-used-first across the 10 pairings, then
        # hash-order across acts; hash-orient which priority EASY sacrifices.
        ordered_pairs = self._least_used(
            self.all_pairs, self.pair_usage, ep_id, "pairs")
        four = ordered_pairs[:4]
        act_pairs = self._hash_order(four, ep_id, "actpairs")
        for p in four:
            self.pair_usage[p] += 1

        acts = []
        for i, (t1, t2) in enumerate(act_tags):
            a, b = act_pairs[i]
            if stable_int(f"{ep_id}:orient:{i}") % 2:
                a, b = b, a
            acts.append({
                "act": i + 1,
                "tags": [self._tag_brief(t1), self._tag_brief(t2)],
                "priority_pair": {
                    "priorities": [a, b],
                    "easy": {"sacrifices": a},
                    "medium": {"sacrifices": b},
                    "hard": {"bypasses": True},
                    "note": ("Situation where the two priorities conflict. "
                             "Easy and medium each sacrifice one priority; "
                             "hard bypasses the dilemma."),
                },
            })

        # Foregrounded character: least-used-first; full cast priority order
        # is the foreground plus the rest in hash order (no fixed adjacency).
        fg = self._least_used(
            self.party_ids, self.foreground_usage, ep_id, "foreground")[0]
        self.foreground_usage[fg] += 1
        rest = self._hash_order([c for c in self.party_ids if c != fg],
                                ep_id, "castorder")
        cast_order = [fg] + rest

        # Places: the foregrounded character's 3 places in hash priority order;
        # each carries its private plan and its NPC extras (with plans).
        place_ids = self._hash_order(CHARACTER_PLACES[fg], ep_id, "places")
        places = []
        for pid in place_ids:
            extras = [
                {
                    "id": ex,
                    "name": self._char_name(ex),
                    "private_plan": load_plan(ex),
                }
                for ex in PLACE_EXTRAS.get(pid, [])
            ]
            places.append({
                "id": pid,
                "name": self._place_name(pid),
                "private_plan": load_plan(pid),
                "extras": extras,
            })

        return {
            "episode_id": ep_id,
            "foregrounded": {
                "id": fg,
                "name": self._char_name(fg),
                "private_plan": load_plan(fg),
                "reveal_one_facet": ("Reveal ONE facet of this character's "
                                     "backstory and personality; advance or "
                                     "plant ONE of their subplots."),
            },
            "cast_priority_order": cast_order,
            "cast_plans": {c: load_plan(c) for c in cast_order},
            "places_in_priority_order": places,
            "consumption_rule": ("Whenever the party travels to a new location, "
                                 "use the first unused location. When an NPC "
                                 "enters, use the first unused extra. "
                                 "place_veranda is the hub: available in every "
                                 "episode, never foregrounded."),
            "pc": {"id": "char_pricha",
                   "name": "Pricha (Lek)",
                   "priorities_all_10_pairs": [
                       {"pair": list(p),
                        "conflict": self._pair_conflict(p)} for p in self.all_pairs]},
            "acts": acts,
        }

    # -- helpers -------------------------------------------------------------

    def _tag_family(self, tag_id: str) -> str:
        """Tag family = name minus trailing _N index (tag_198/tag_202 -> 'standing')."""
        tag = next(t for t in self.tags if t["id"] == tag_id)
        import re
        return re.sub(r"_\d+$", "", tag["name"])

    def _tag_brief(self, tag_id: str) -> dict:
        tag = next(t for t in self.tags if t["id"] == tag_id)
        themes = []
        for vid in tag.get("vocab_item_ids", [])[:3]:
            vocab = self._vocab.get(vid)
            if vocab:
                themes.append(vocab.get("english", ""))
        return {"id": tag_id, "name": tag["name"], "themes": themes}

    def _pair_conflict(self, pair) -> str:
        names = {a["id"]: a["name"] for a in self.attributes}
        return f"{names[pair[0]]} vs {names[pair[1]]}"

    def _char_name(self, char_id: str) -> str:
        return next((c["name"] for c in self.characters if c["id"] == char_id), char_id)

    def _place_name(self, place_id: str) -> str:
        return next((p["name"] for p in self.places if p["id"] == place_id), place_id)


# ---------------------------------------------------------------------------
# Selftest: prove even distribution + no rotation artifacts + determinism.
# ---------------------------------------------------------------------------

def selftest() -> None:
    # Uniform start (no existing episodes): greedy least-used-first yields
    # exact evenness whenever the total slots divide evenly.
    data = _load_data()
    data["episodes"] = []
    scheduler = Scheduler(data, start_ep=341)

    # Four full tag cycles; long enough for meaningful place-order stats
    # (each character foregrounded ~28x).
    count = 4 * len(scheduler.tags) // 8  # = 170 episodes -> each tag exactly 4x
    first = [scheduler.deal(341 + i) for i in range(count)]
    sched2 = Scheduler(_load_data() | {"episodes": []}, start_ep=341)
    second = [sched2.deal(341 + i) for i in range(count)]

    # 1. Determinism.
    assert first == second, "scheduler is not deterministic"

    # 2. Even tag distribution: each tag used exactly `count*8/340` times.
    total_slots = count * 8
    per_tag = total_slots / len(scheduler.tags)
    for tag_id, n in scheduler.tag_usage.items():
        assert n == per_tag, f"tag {tag_id} used {n}x, expected {per_tag}"

    # 3. Even priority-pair distribution (+-1 at all times, exact at end).
    for pair, n in scheduler.pair_usage.items():
        assert abs(n - count * 4 / 10) < 1, f"pair {pair} used {n}x"

    # 4. Even foregrounding: 6 characters, 85 episodes -> max-min <= 1,
    #    and no character follows a fixed other character (rotation would
    #    produce a fixed successor ~100% of the time; hash ordering ~1/5).
    fg_seq = [p["foregrounded"]["id"] for p in first]
    counts = {c: fg_seq.count(c) for c in scheduler.party_ids}
    assert max(counts.values()) - min(counts.values()) <= 1, counts
    transitions = list(zip(fg_seq, fg_seq[1:]))
    for a in scheduler.party_ids:
        for b in scheduler.party_ids:
            if a == b:
                continue
            share = transitions.count((a, b)) / len(transitions)
            assert share < 0.30, f"predictable transition {a} -> {b}: {share:.0%}"

    # 5. No-rotation check.  A rotating scheme makes the NEXT episode's order
    #    a cyclic rotation of the current one 100% of the time; a hash
    #    permutation does so only by rare coincidence.  We assert the
    #    consecutive-rotation share is far below rotation levels, and that
    #    adjacency (who sits next to whom in the priority list) is flat.
    def is_rotation(x, y):
        return len(x) == len(y) and all(
            y[i:] + y[:i] == x for i in range(len(y)))
    orders = [p["cast_priority_order"] for p in first]
    consec_rot = sum(
        1 for i in range(len(orders) - 1)
        if is_rotation(orders[i], orders[i + 1])) / (len(orders) - 1)
    assert consec_rot <= 0.10, f"consecutive rotation share {consec_rot:.0%}"
    from collections import Counter
    adjacent = Counter()
    for o in orders:
        for a, b in zip(o, o[1:]):
            adjacent[tuple(sorted((a, b)))] += 1
    n_adj = sum(adjacent.values())
    uniform = 1 / (len(scheduler.party_ids) * (len(scheduler.party_ids) - 1) / 2)
    worst = max(adjacent.values()) / n_adj
    assert worst <= 2 * uniform, (
        f"adjacency not flat: worst pair {worst:.0%} vs uniform {uniform:.0%}")

    # 6. Place priority orders vary per character: every place takes first
    #    position sometimes; at least 5 of 6 permutations appear each.
    by_char = {}
    for p in first:
        by_char.setdefault(p["foregrounded"]["id"], []).append(
            tuple(pl["id"] for pl in p["places_in_priority_order"]))
    for c, seqs in by_char.items():
        firsts = {s[0] for s in seqs}
        assert firsts == set(CHARACTER_PLACES[c]), (
            f"{c}: places never first: {set(CHARACTER_PLACES[c]) - firsts}")
        assert len(set(seqs)) >= 5, f"{c}: only {len(set(seqs))} place orders"

    print("SELFTEST PASS")
    print(f"  {count} episodes dealt")
    print(f"  tags: {len(scheduler.tags)} tags, each used exactly "
          f"{int(per_tag)}x (uniform start)")
    print(f"  pairs: each of 10 pairs used "
          f"{sorted(set(scheduler.pair_usage.values()))}x")
    print(f"  foregrounds: {counts}")
    print(f"  max predictable transition share: "
          f"{max(transitions.count(t) for t in set(transitions)) / len(transitions):.0%}"
          f" (rotation would be 100%)")
    print(f"  consecutive cast-order rotations: {consec_rot:.1%} (rotation scheme: 100%)")
    print(f"  worst adjacency share: {worst:.1%} (uniform: {uniform:.1%})")
    print(f"  distinct cast orders: {len(set(tuple(o) for o in orders))}")


def _load_data() -> dict:
    return {
        "episodes": load_json(EPISODES_PATH) if EPISODES_PATH.exists() else [],
        "tags": load_json(TAGS_PATH),
        "vocab": load_json(VOCAB_PATH),
        "attributes": load_json(ATTRIBUTES_PATH),
        "characters": load_json(CHARACTERS_PATH),
        "places": load_json(PLACES_PATH),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", type=int, default=None,
                    help="first episode number (default: existing count + 1)")
    ap.add_argument("--count", type=int, default=1,
                    help="number of episode packages to deal")
    ap.add_argument("--out", type=Path, default=None,
                    help="output JSON path (default: stdout)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    data = _load_data()
    start = args.start if args.start is not None else len(data["episodes"]) + 1
    scheduler = Scheduler(data, start_ep=start)
    packages = [scheduler.deal(start + i) for i in range(args.count)]
    out = json.dumps(packages, ensure_ascii=False, indent=1)
    if args.out:
        args.out.write_text(out, encoding="utf-8")
        print(f"wrote {args.count} package(s) to {args.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
