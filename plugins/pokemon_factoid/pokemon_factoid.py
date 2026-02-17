import random
import textwrap
import time
from urllib.request import Request, urlopen
import json

from PIL import Image, ImageDraw, ImageFont

from src.plugins.base_plugin import BasePlugin


class PokemonFactoid(BasePlugin):
    """Display a Pokémon fact that refreshes every 5 minutes."""

    FACT_TTL_SECONDS = 300
    MAX_POKEMON_ID = 1025

    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params["style_settings"] = True
        return template_params

    def generate_image(self, settings, device_config):
        width = device_config.get_resolution_x()
        height = device_config.get_resolution_y()

        force_refresh = str(settings.get("force_refresh", "false")).lower() in {
            "true",
            "1",
            "on",
            "yes",
        }

        fact_data = self._get_fact_data(settings, force_refresh)

        image = Image.new("1", (width, height), 255)
        draw = ImageDraw.Draw(image)

        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

        margin = 10
        y = margin

        draw.text((margin, y), "Pokemon Factoid", fill=0, font=title_font)
        y += 18

        subtitle = "Refreshes every 5 minutes"
        draw.text((margin, y), subtitle, fill=0, font=footer_font)
        y += 18

        usable_width = max(20, width - (margin * 2))
        wrapped_fact = self._wrap_text(fact_data["fact"], body_font, usable_width)

        for line in wrapped_fact:
            if y > height - 35:
                break
            draw.text((margin, y), line, fill=0, font=body_font)
            y += 12

        age_seconds = int(time.time() - fact_data["updated_at"])
        footer = f"#{fact_data['pokemon_id']} {fact_data['pokemon_name'].title()} · {age_seconds // 60}m ago"
        draw.text((margin, height - 16), footer, fill=0, font=footer_font)

        # Clear one-shot action after use.
        settings["force_refresh"] = "false"

        return image

    def _get_fact_data(self, settings, force_refresh):
        now = int(time.time())
        cached_fact = settings.get("last_fact", "")
        cached_name = settings.get("last_pokemon", "")
        cached_id = int(settings.get("last_pokemon_id", 0) or 0)
        updated_at = int(settings.get("last_updated_epoch", 0) or 0)

        is_fresh = (
            cached_fact
            and cached_name
            and cached_id > 0
            and (now - updated_at) < self.FACT_TTL_SECONDS
        )

        if is_fresh and not force_refresh:
            return {
                "fact": cached_fact,
                "pokemon_name": cached_name,
                "pokemon_id": cached_id,
                "updated_at": updated_at,
            }

        try:
            pokemon_id, pokemon_name, fact = self._fetch_random_fact()
            settings["last_fact"] = fact
            settings["last_pokemon"] = pokemon_name
            settings["last_pokemon_id"] = pokemon_id
            settings["last_updated_epoch"] = now

            return {
                "fact": fact,
                "pokemon_name": pokemon_name,
                "pokemon_id": pokemon_id,
                "updated_at": now,
            }
        except Exception:
            if cached_fact and cached_name:
                return {
                    "fact": f"{cached_fact} (offline cache)",
                    "pokemon_name": cached_name,
                    "pokemon_id": max(cached_id, 0),
                    "updated_at": updated_at or now,
                }
            raise RuntimeError(
                "Unable to fetch Pokemon fact. Check internet connection or API availability."
            )

    def _fetch_random_fact(self):
        pokemon_id = random.randint(1, self.MAX_POKEMON_ID)
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/"

        response = self._http_get_json(url)

        pokemon_name = response.get("name", f"pokemon-{pokemon_id}")
        flavor_entries = response.get("flavor_text_entries", [])

        english_entries = [
            e
            for e in flavor_entries
            if e.get("language", {}).get("name") == "en" and e.get("flavor_text")
        ]

        if not english_entries:
            raise RuntimeError("No English flavor text available for selected Pokémon.")

        selected = random.choice(english_entries)
        fact = self._normalize_fact(selected["flavor_text"])

        return pokemon_id, pokemon_name, fact

    def _http_get_json(self, url):
        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "inkypi-pokemon-factoid/1.0",
            },
        )

        with urlopen(request, timeout=15) as response:
            payload = response.read()

        return json.loads(payload.decode("utf-8"))

    @staticmethod
    def _normalize_fact(raw_fact):
        cleaned = raw_fact.replace("\n", " ").replace("\f", " ")
        return " ".join(cleaned.split())

    @staticmethod
    def _wrap_text(text, font, max_width):
        # Conservative character estimate for PIL default font.
        approx_chars = max(10, max_width // 6)
        return textwrap.wrap(text, width=approx_chars)
