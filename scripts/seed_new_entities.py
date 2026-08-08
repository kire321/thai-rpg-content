#!/usr/bin/env python3
"""Add the next ten reusable NPCs and ten acoustically distinct places.

The repository keeps the catalog in JSON and serves pictures from /public.  The
small procedural illustrations are deliberately deterministic so the content
can be regenerated without a separate image service.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

NEW_CHARACTERS = [
    {
        "id": "char_kanya",
        "name": "Kanya",
        "picture": "/characters/kanya.png",
        "type": "npc",
        "description": "An anchor keeper who tunes the great moorings beneath Khrueang. Kanya hears a failing tether as a change in the floor's pulse and quietly records which officials ignore the warning.",
    },
    {
        "id": "char_wichai",
        "name": "Wichai",
        "picture": "/characters/wichai.png",
        "type": "npc",
        "description": "A resonance diver who descends through temporary channels to recover crystal cores. He is cheerful in danger, but every dive has left him with a different memory of the lattice.",
    },
    {
        "id": "char_maliwan",
        "name": "Maliwan",
        "picture": "/characters/maliwan.png",
        "type": "npc",
        "description": "A surface medic who runs a moving clinic on a reinforced harvest platform. Maliwan treats resonance sickness with practical remedies and insists that skycity patients learn the warning signs themselves.",
    },
    {
        "id": "char_jintana",
        "name": "Jintana",
        "picture": "/characters/jintana.png",
        "type": "npc",
        "description": "A junior clerk in the Tonal Orders who copies route permits by day and leaks censored frequencies by night. Her precise memory makes her a dangerous witness when the Orders rewrite a record.",
    },
    {
        "id": "char_sakchai",
        "name": "Sakchai",
        "picture": "/characters/sakchai.png",
        "type": "npc",
        "description": "A pirate navigator who can read a storm's harmonics from the vibration of a ship's rails. Sakchai wants out of the raiding life, but a hidden debt keeps pulling him back to the sky lanes.",
    },
    {
        "id": "char_pailin",
        "name": "Pailin",
        "picture": "/characters/pailin.png",
        "type": "npc",
        "description": "A crystal artisan whose bowls preserve a spoken tone for several minutes. Pailin sells beautiful work to the Orders while hiding a workshop where Groundless families share forbidden tools.",
    },
    {
        "id": "char_rung",
        "name": "Rung",
        "picture": "/characters/rung.png",
        "type": "npc",
        "description": "A Groundless organizer who builds safe surface shelters from ship ribs and lattice glass. Rung is an eloquent advocate for permanent settlement, yet refuses to send volunteers where the numbers are uncertain.",
    },
    {
        "id": "char_nop",
        "name": "Nop",
        "picture": "/characters/nop.png",
        "type": "npc",
        "description": "An archive conservator who repairs damaged route tablets with patient, nearly silent taps. Nop remembers every missing page and suspects the oldest gaps describe a deliberate experiment.",
    },
    {
        "id": "char_chaiyo",
        "name": "Chaiyo",
        "picture": "/characters/chaiyo.png",
        "type": "npc",
        "description": "A storm cartographer who maps wind shear by singing into glass kites. Chaiyo trades accurate forecasts for access to unredacted charts and never leaves a route unmarked.",
    },
    {
        "id": "char_lalida",
        "name": "Lalida",
        "picture": "/characters/lalida.png",
        "type": "npc",
        "description": "A skybridge courier who carries letters between islands on a tuned cable cart. Lalida knows the private entrances of every terminal and uses ordinary deliveries to move people the Orders would detain.",
    },
]

NEW_PLACES = [
    {
        "id": "place_moonwell_platform",
        "name": "Moonwell Platform",
        "picture": "/places/moonwell_platform.png",
        "description": "A circular maintenance platform surrounds a vertical crystal well that repeats every sound after a long, luminous pause. The delayed echoes expose hidden conversations and make hurried tonal work dangerous, ideal for patient investigations and tense testimony.",
    },
    {
        "id": "place_iron_kite_docks",
        "name": "Iron Kite Docks",
        "picture": "/places/iron_kite_docks.png",
        "description": "Cargo kites moor to iron spars above a roaring updraft, their cables singing different notes under load. Crews can repair engines and bargain for passage here, but one wrong vibration can turn a routine launch into a rescue.",
    },
    {
        "id": "place_singing_rice_terraces",
        "name": "Singing Rice Terraces",
        "picture": "/places/singing_rice_terraces.png",
        "description": "Floating rice beds ripple in ordered waves, producing a soft chord whenever the wind crosses the stalks. Farmers use the living rhythm to detect lattice storms, making the terraces a peaceful refuge and an early-warning station.",
    },
    {
        "id": "place_undertone_bazaar",
        "name": "Undertone Bazaar",
        "picture": "/places/undertone_bazaar.png",
        "description": "A market built beneath a suspended island amplifies low voices while swallowing high ones. Smugglers, clerks, and informants meet under its acoustic blind spot, where a carefully chosen phrase can reveal more than a shouted accusation.",
    },
    {
        "id": "place_lattice_fisheries",
        "name": "Lattice Fisheries",
        "picture": "/places/lattice_fisheries.png",
        "description": "Scavenger platforms drift over a shallow field of liquid crystal where resonance fish follow familiar melodies. Harvesters must keep a steady call while moving between transparent shelves, creating room for survival work, ethical arguments, and sudden storms.",
    },
    {
        "id": "place_bellflower_observatory",
        "name": "Bellflower Observatory",
        "picture": "/places/bellflower_observatory.png",
        "description": "A ring of bell-shaped instruments hangs from an observation tower and rings when the lattice geometry shifts. Cartographers come for precise measurements, while the Orders come to control what the bells are allowed to say.",
    },
    {
        "id": "place_broken_tether_field",
        "name": "Broken Tether Field",
        "picture": "/places/broken_tether_field.png",
        "description": "Fragments of failed resonance anchors float in a slow spiral below a deserted island. Each shard carries a different remembered tone, turning navigation into a hazardous act of listening and offering clues about abandoned skycities.",
    },
    {
        "id": "place_echo_cistern",
        "name": "Echo Cistern",
        "picture": "/places/echo_cistern.png",
        "description": "An old water reservoir beneath a farming district returns speech from the wrong direction. Its clean acoustics are useful for rehearsing tonal phrases, but the borrowed voices have begun answering questions no one asked.",
    },
    {
        "id": "place_cloudstep_village",
        "name": "Cloudstep Village",
        "picture": "/places/cloudstep_village.png",
        "description": "A small settlement hangs from a chain of buoyant stone steps, and every footfall makes the homes sway in sympathy. Residents rely on communal songs to keep the steps aligned, making any dispute immediately physical.",
    },
    {
        "id": "place_resonant_greenhouse",
        "name": "Resonant Greenhouse",
        "picture": "/places/resonant_greenhouse.png",
        "description": "A sealed greenhouse grows crystal-veined plants under a carefully tuned canopy. Its leaves filter harmful frequencies from the air, while a locked inner room preserves a living record of the Silencing.",
    },
]


def stable_color(seed: str) -> tuple[int, int, int]:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return (45 + digest[0] % 100, 55 + digest[1] % 100, 80 + digest[2] % 100)


def font(size: int):
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw_label(draw: ImageDraw.ImageDraw, label: str, width: int, y: int, size: int = 24):
    f = font(size)
    # Keep the generated label legible without needing a font with Thai glyphs.
    label = label.upper()
    while draw.textbbox((0, 0), label, font=f)[2] > width - 48 and len(label) > 8:
        label = label[:-4] + "..."
    box = draw.textbbox((0, 0), label, font=f)
    x = (width - (box[2] - box[0])) // 2
    draw.rounded_rectangle((x - 14, y - 8, x + box[2] - box[0] + 14, y + box[3] - box[1] + 8), radius=10, fill=(8, 15, 35, 205))
    draw.text((x, y), label, fill=(240, 248, 255), font=f)


def make_character_image(item: dict, index: int):
    width = height = 512
    base = stable_color(item["id"])
    image = Image.new("RGB", (width, height), base)
    draw = ImageDraw.Draw(image, "RGBA")
    # Atmospheric rings suggest the setting's resonance without claiming to be a portrait.
    for radius in range(90, 310, 42):
        alpha = max(16, 100 - radius // 4)
        draw.ellipse((256 - radius, 205 - radius, 256 + radius, 205 + radius), outline=(170, 235, 255, alpha), width=4)
    accent = stable_color(item["name"] + str(index))
    # Head and shoulders silhouette.
    draw.ellipse((188, 92, 324, 228), fill=(*accent, 255), outline=(230, 250, 255, 210), width=4)
    draw.polygon([(135, 470), (154, 330), (207, 270), (305, 270), (358, 330), (380, 470)], fill=(*accent, 235))
    draw.arc((150, 282, 362, 510), 180, 360, fill=(240, 250, 255, 180), width=5)
    # Small tuning marks.
    for x in (78, 430):
        draw.line((x, 112, x, 300), fill=(220, 248, 255, 150), width=3)
        draw.ellipse((x - 10, 180, x + 10, 200), fill=(220, 248, 255, 180))
    draw_label(draw, item["name"], width, 438, 22)
    image.save(PUBLIC / "characters" / Path(item["picture"]).name, format="PNG", optimize=True)


def make_place_image(item: dict, index: int):
    width, height = 768, 432
    top = stable_color(item["id"] + "sky")
    bottom = stable_color(item["id"] + "crystal")
    image = Image.new("RGB", (width, height))
    px = image.load()
    for y in range(height):
        ratio = y / (height - 1)
        color = tuple(int(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
        for x in range(width):
            px[x, y] = color
    draw = ImageDraw.Draw(image, "RGBA")
    # Floating island silhouette and resonant crystal spires.
    horizon = 265 + (index % 4) * 8
    draw.polygon([(0, horizon), (110, horizon - 18), (205, horizon + 10), (330, horizon - 28), (470, horizon + 3), (620, horizon - 20), (768, horizon + 5), (768, height), (0, height)], fill=(10, 20, 45, 210))
    for i in range(9):
        x = 45 + ((i * 97 + index * 31) % 680)
        h = 45 + ((i * 29 + index * 17) % 115)
        w = 18 + (i % 3) * 8
        crystal = stable_color(item["name"] + str(i))
        draw.polygon([(x, horizon + 8), (x + w // 2, horizon - h), (x + w, horizon + 8)], fill=(*crystal, 205), outline=(205, 245, 255, 150))
        draw.line((x + w // 2, horizon - h + 8, x + w // 2, horizon + 4), fill=(225, 250, 255, 125), width=2)
    for r in (54, 91, 128):
        draw.arc((width // 2 - r, horizon - 60 - r, width // 2 + r, horizon - 60 + r), 200, 340, fill=(180, 245, 255, 90), width=3)
    draw_label(draw, item["name"], width, 30, 24)
    image.save(PUBLIC / "places" / Path(item["picture"]).name, format="PNG", optimize=True)


def append_unique(path: Path, additions: list[dict]):
    data = json.loads(path.read_text(encoding="utf-8"))
    existing = {item["id"] for item in data}
    for item in additions:
        if item["id"] not in existing:
            data.append(item)
            existing.add(item["id"])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def main():
    chars = append_unique(PUBLIC / "characters.json", NEW_CHARACTERS)
    places = append_unique(PUBLIC / "places.json", NEW_PLACES)
    (PUBLIC / "characters").mkdir(exist_ok=True)
    (PUBLIC / "places").mkdir(exist_ok=True)
    for i, item in enumerate(NEW_CHARACTERS):
        make_character_image(item, i)
    for i, item in enumerate(NEW_PLACES):
        make_place_image(item, i)
    print(f"characters: {len(chars)}; places: {len(places)}")
    print("generated deterministic character and place artwork")


if __name__ == "__main__":
    main()
