# Saskatoon Art Guide

A collaborative, living catalog of public art and murals in Saskatoon and Saskatchewan.

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

### Submitting New Artworks

1. Review the schema in `data/schema/artwork.schema.json`
2. Prepare your submission in JSON format
3. Submit via GitHub pull request or issue

See `governance/workflow.md` for detailed submission guidelines.

### Reporting Corrections

If you notice an error in attribution, location, or other details, please open an issue or contact the curator directly. Attribution corrections are prioritized.

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
