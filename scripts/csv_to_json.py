import csv
import json
from pathlib import Path

INPUT_CSV = "submissions.csv"
OUTPUT_JSON = "data/artworks/saskatoon_from_submissions.json"

def parse_medium(value):
    if not value:
        return []
    return [m.strip().lower().replace(" ", "_") for m in value.split(",")]

artworks = []

with open(INPUT_CSV, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        artwork = {
            "title": row.get("Artwork Title", "").strip(),
            "artist": row.get("Artist Name(s)", "").strip(),
            "year": int(row["Year Completed"]) if row.get("Year Completed") else None,
            "location": {
                "address": row.get("Location", "").strip(),
                "neighbourhood": row.get("Neighbourhood", "").strip(),
                "latitude": float(row["Latitude"]) if row.get("Latitude") else None,
                "longitude": float(row["Longitude"]) if row.get("Longitude") else None
            },
            "commissioned_by": row.get("Commissioning Body", "").strip(),
            "medium": parse_medium(row.get("Medium", "")),
            "artist_contact": row.get("Artist Contact", "").strip(),
            "source": row.get("Source", "").strip(),
            "status": row.get("Status", "").strip().lower()
        }

        artworks.append(artwork)

output_path = Path(OUTPUT_JSON)
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as jsonfile:
    json.dump(artworks, jsonfile, indent=2, ensure_ascii=False)

print(f"Converted {len(artworks)} submissions to {OUTPUT_JSON}")
