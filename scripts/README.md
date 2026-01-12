# Scripts

This directory contains automation tools for artwork discovery and submission processing.

## Discovery Pipeline

### discover_artworks.py

Discovers public artworks from various online sources and outputs candidates to CSV.

**Features:**
- Scrapes DTNYXE blog for mural announcements
- Extracts artist names, titles, locations, and years
- Assigns confidence scores (high/medium/low)
- Avoids duplicates
- Respects rate limiting

**Usage:**
```bash
python3 scripts/discover_artworks.py
```

**Output:**
- `data/discovered/candidates.csv` - Discovered artworks with metadata
- `data/discovered/sources.json` - Source reliability information
- `data/discovered/discovery.log` - Detailed execution log
- `data/discovered/discovery_report.md` - Human-readable summary

**Current Sources:**
- DTNYXE Downtown Blog
- (More sources can be added)

### find_artist_contacts.py

Finds public contact information for artists discovered in the catalog.

**Features:**
- Searches for artist websites
- Suggests Instagram profiles
- Notes artist directory listings
- Respects privacy and rate limits

**Usage:**
```bash
python3 scripts/find_artist_contacts.py
```

**Output:**
- `data/discovered/contacts.json` - Artist contact information

**Privacy Policy:**
- Only uses publicly available information
- Respects robots.txt and rate limits
- No scraping of private profiles
- Follows platform Terms of Service

## Bulk Submission Processing

### csv_to_json.py

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
