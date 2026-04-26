# VersionLink

VersionLink is a lightweight Flask app that helps you find the best shared **Minecraft version + mod loader** for a list of mods.

Paste mod slugs, run an analysis, and get:
- Recommended compatible config(s)
- A list of incompatible mods (if any)
- Quick manifest export/import options

## What It Does

VersionLink checks each mod's supported configurations and then:
1. Tries to find a perfect intersection across all mods.
2. If no perfect match exists, picks the most common "best-fit" config and reports which mods do not support it.

This makes it easy to decide what environment to target before building a modpack.

## Stack

- Python + Flask
- Requests for API calls
- Flask-Caching (filesystem cache)
- Tailwind CSS (via CDN)

## Quick Start

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open:

```text
http://localhost:5000
```

## How To Use

1. Enter one Modrinth slug per line (for example: `sodium`, `lithium`).
2. Click **Analyze Compatibility**.
3. Review recommended configs and any incompatible mods.
4. Optionally export/import mod lists (`.txt` or advanced `.json`).

## API Endpoint

`POST /check`

Example request body:

```json
{
  "mods": [
    { "platform": "modrinth", "id": "sodium" },
    { "platform": "modrinth", "id": "lithium" }
  ]
}
```

Example response fields:
- `recommended_configs`
- `incompatible_mods`
- `found_mods`
- `not_found`
- `status`

## Notes

- Caching is enabled with a filesystem backend in `cache-directory/` (default timeout: 1 hour).
- The UI currently submits Modrinth slugs by default.
- CurseForge API support exists in code, but requires an API key integration flow to be fully wired into app startup/UI.

## Project Layout

```text
app.py              # Flask routes + compatibility endpoint
api_client.py       # Mod platform API integration
mod_state.py        # Compatibility analysis logic
templates/index.html# Frontend UI
cache-directory/    # Cached API responses
```

---

If you want, I can also add a short **Troubleshooting** section and a **Roadmap** section (CurseForge key config, multi-platform UI, Docker setup).