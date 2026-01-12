# Scripts

This directory contains automation tools for processing artwork submissions.

## csv_to_json.py

Converts CSV submissions to JSON format matching the artwork schema.

### Usage

1. Place `submissions.csv` in the repo root
2. From the repo root, run:
   ```bash
   python3 scripts/csv_to_json.py
   ```
3. Output file will be created at:
   ```
   data/artworks/saskatoon_from_submissions.json
   ```

### Expected CSV Format

The CSV must include these columns:

- Artwork Title
- Artist Name(s)
- Year Completed
- Location
- Neighbourhood
- Latitude
- Longitude
- Commissioning Body
- Medium
- Artist Contact
- Source
- Status

### REQUIRED: Manual Review Step (Non-Negotiable)

**DO NOT merge `saskatoon_from_submissions.json` automatically into `saskatoon.json`.**

Before committing any converted data:

1. Open `saskatoon_from_submissions.json`
2. Check:
   - Artist names spelled correctly
   - No missing titles
   - Medium values make sense
   - Status is one of: `active`, `removed`, `altered`
   - Coordinates are accurate
   - Source information is credible
3. Manually copy vetted entries into:
   ```
   data/artworks/saskatoon.json
   ```

### Why This Design Is Intentional

This script:

- **Does not auto-publish** — Prevents attribution errors
- **Preserves human judgment** — Curator reviews before publication
- **Keeps GitHub as the source of truth** — No external dependencies
- **Scales to hundreds of entries** — Reduces manual data entry
- **Can later be wrapped in automation** — If needed with proper safeguards

This is cultural infrastructure, not a content firehose. Attribution accuracy and trust are non-negotiable.
