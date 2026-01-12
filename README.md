# Saskatoon Art Guide

A collaborative, living catalog of public art and murals in Saskatoon and Saskatchewan.

This repository is an open data catalog. It is governed by a neutral attribution policy and is open for community contributions via GitHub issues and pull requests.

## What This Is

The Saskatoon Art Guide is a structured, open dataset documenting public artworks across the city and region. It prioritizes:

- Accurate attribution to artists
- Neutral, factual documentation
- Community collaboration
- Long-term preservation of records

This is infrastructure, not branding. It is a shared resource for residents, visitors, researchers, and the artistic community.

## What This Is Not

This is not a portfolio. It is not owned or controlled by any single person. It does not rank, review, or editorialize about artworks.

## Who It's For

- **Artists** documenting their own work
- **Residents and visitors** exploring public art
- **Researchers** studying urban art and culture
- **Developers** building apps, maps, or tools using public art data
- **Organizations** tracking commissioned works

## Data Structure

All artworks are documented using a canonical JSON schema located in `data/schema/artwork.schema.json`.

Each entry includes:

- Title and artist name(s)
- Location and GPS coordinates
- Year completed
- Medium and commissioning information
- Source of information
- Current status (active, removed, or altered)

## How to Contribute

Contributions are welcome from anyone with accurate information about public art.

Contributions are handled via GitHub issues or pull requests only. Please use the provided templates when submitting new works or corrections.

### Submitting New Artworks

1. Review the schema in `data/schema/artwork.schema.json`
2. Prepare your submission in JSON format
3. Submit via GitHub pull request or issue

See `governance/workflow.md` for detailed submission guidelines.

### Reporting Corrections

If you notice an error in attribution, location, or other details, please open an issue or contact the curator directly. Attribution corrections are prioritized.

## Tools and Automation

### Issue Templates

The repository includes structured issue templates to streamline contributions:

- **New Artwork Submission** — Submit a new artwork with required fields
- **Correction or Update** — Report errors in existing entries

These templates ensure consistent data formatting and make it easier for the community to contribute.

### Bulk Submission Processing

For processing multiple artworks at once, use the CSV to JSON conversion script:

```bash
# 1. Prepare submissions.csv in repo root
# 2. Run conversion script
python3 scripts/csv_to_json.py

# 3. Review output at data/artworks/saskatoon_from_submissions.json
# 4. Manually verify and merge vetted entries into saskatoon.json
```

See `scripts/README.md` for detailed usage instructions and CSV format requirements.

**Important:** The conversion script does not auto-publish. All entries must be manually reviewed before adding to the catalog to ensure attribution accuracy.

### Automation Roadmap

A phased automation plan is under development to scale the catalog while maintaining quality:

- **Phase 1:** Automated discovery from public sources
- **Phase 2:** Artist contact information finding
- **Phase 3:** Ethical outreach with artist verification
- **Phase 4:** Response processing and staging
- **Phase 5:** GitHub integration for batch updates

See `governance/automation-plan.md` for the complete roadmap and ethical safeguards.

## Governance

This project is maintained by Josh Jacobson as steward and curator. Governance documents are located in the `governance/` directory:

- `mission.md` — Purpose and principles
- `attribution.md` — Attribution policy
- `workflow.md` — Submission and correction process

## Emerging Practices

The guide tracks traditional murals and paintings as well as emerging formats including XR (extended reality) and WebAR-based public art installations.

## License and Use

This catalog is intended for public use. When using this data:

- Always credit the original artist
- Do not imply endorsement by the guide or its maintainers
- Preserve attribution when republishing or adapting the data

## Contact

For submissions, corrections, or questions, open an issue on this repository or visit [jjacobsondesign.ca](https://www.jjacobsondesign.ca).
