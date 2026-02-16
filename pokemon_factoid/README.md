# Pokémon Factoid plugin

This repo intentionally **does not commit binary files** (like `icon.png`) because the current review/transfer pipeline rejects binaries.

## Important: generate icon locally after clone
Run this once inside `pokemon_factoid/`:

```bash
python generate_icon.py
```

That creates `icon.png` locally so InkyPi can display the plugin icon.

## Why "failed to clone repository" happens
InkyPi installs third-party plugins by cloning a git URL. Clone fails if the URL is missing, empty, private, or unreachable from the device.

## Install options

### Option A: Local plugin install
1. Copy `pokemon_factoid/` into InkyPi `src/plugins/`.
2. Run `python generate_icon.py` in that folder.
3. Restart InkyPi service.

### Option B: Third-party plugin repo
1. Put this plugin in its own public git repository.
2. Ensure the repository URL entered in InkyPi is publicly reachable.
3. After clone, run `python generate_icon.py` on-device.

## Required files
- `pokemon_factoid.py`
- `plugin-info.json`
- `settings.html`
- `generate_icon.py` (creates local `icon.png`)
