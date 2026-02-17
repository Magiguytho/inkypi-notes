# Pokémon Factoid plugin

This repo intentionally **does not commit binary files** (like `icon.png`) because the current review/transfer pipeline rejects binaries.

## Fix for your current clone error

## EXACT value to paste into InkyPi

Paste **exactly** this (no extra path):

```
https://github.com/Magiguytho/inkypi-notes.git
```

Do **NOT** use:

```
https://github.com/Magiguytho/inkypi-notes/tree/main/pokemon_factoid
```

You used:

- `https://github.com/Magiguytho/inkypi-notes/tree/main/pokemon_factoid`

That is a **web page URL**, not a git clone URL.

Use the repository clone URL instead:

- `https://github.com/Magiguytho/inkypi-notes.git`

InkyPi will clone the repo and then discover the `pokemon_factoid/` plugin folder.

## Important: generate icon locally after clone
Run this once inside `pokemon_factoid/`:

```bash
python generate_icon.py
```

That creates `icon.png` locally so InkyPi can display the plugin icon.

## Why "failed to clone repository" happens
InkyPi installs third-party plugins by cloning a git URL. Clone fails if the URL is missing, empty, private, unreachable, or is a non-git webpage URL (`.../tree/...`).

## Install options

### Option A: Third-party install via repository URL
1. In InkyPi, add repository URL: `https://github.com/Magiguytho/inkypi-notes.git`
2. Let InkyPi clone and discover `pokemon_factoid/`.
3. Run `python generate_icon.py` in the plugin folder on-device.
4. Restart InkyPi service.

### Option B: Local plugin install
1. Copy `pokemon_factoid/` into InkyPi `src/plugins/`.
2. Run `python generate_icon.py` in that folder.
3. Restart InkyPi service.

## Required files
- `pokemon_factoid.py`
- `plugin-info.json`
- `settings.html`
- `generate_icon.py` (creates local `icon.png`)
