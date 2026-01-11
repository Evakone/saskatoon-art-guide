# Contribution and Correction Workflow

The Saskatoon Art Guide is a collaborative catalog. Submissions and corrections are welcome from artists, community members, and observers.

## Who Can Submit

- Artists documenting their own work
- Community members who have observed public art
- Researchers or historians with verifiable information
- Organizations that commissioned artworks

## Required Metadata

All submissions must include:

- **title**: The name of the artwork (if known, or a descriptive title)
- **artist**: The full name(s) of the artist(s)
- **location**: Street address or specific location description
- **source**: How this information was obtained

Recommended but optional:

- **year**: When the artwork was completed
- **commissioned_by**: Organization or individual who commissioned the work
- **medium**: Materials used (paint, vinyl, mixed media, XR, etc.)
- **artist_contact**: Link to artist's website or portfolio
- **latitude/longitude**: GPS coordinates
- **status**: Whether the artwork is active, removed, or altered

## Submission Process

1. Prepare artwork information in JSON format following the schema in `data/schema/artwork.schema.json`
2. Submit via GitHub issue, pull request, or email to the curator
3. Curator reviews for accuracy and adherence to attribution policy
4. Entry is added to the appropriate data file

## Corrections

If you notice an error in attribution, location, or any other detail:

1. Open a GitHub issue or contact the curator directly
2. Provide the correct information and a source if possible
3. Corrections are prioritized and applied immediately

## Attribution Accuracy

All submissions are reviewed to ensure:

- Artists are correctly credited
- No authorship is implied by the guide or its maintainers
- Contact information (if provided) is accurate and current
- The source of information is documented

If attribution cannot be verified, the submission will be held until confirmation is obtained.

## Removal Requests

If an artist requests removal of their work from the catalog, the request will be honored. However, a minimal record (title, artist, year, status: "removed at artist request") may be retained for historical accuracy.
