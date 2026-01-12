# Automation Workflow Plan

## Vision

Build a semi-automated pipeline that discovers public art, finds artist contact information, reaches out for verification, and updates the catalog with minimal curator intervention.

## Phases

### Phase 1: Automated Discovery (Low Risk)

**Goal:** Find public art information from existing sources

**Sources:**
- City of Saskatoon public art registry
- Downtown BID/business district websites
- Local news articles and blogs (e.g., DTNYXE)
- Social media posts (Instagram hashtags: #yxeart, #saskatoonart, #publicartyxe)
- Google Maps reviews/photos
- Tourism Saskatchewan databases

**Tools:**
- Web scraping (BeautifulSoup, Scrapy)
- Social media APIs (Instagram Graph API, Twitter API)
- Google Places API for location data
- News aggregation APIs

**Output:**
- CSV file with discovered artworks
- Confidence score for each field (high/medium/low)
- Source URLs for verification

**Storage:**
```
data/discovered/
├── candidates.csv
└── sources.json
```

### Phase 2: Contact Information Discovery (Medium Risk)

**Goal:** Find artist contact information ethically

**Ethical Considerations:**
- Only use publicly available information
- Respect privacy preferences
- No scraping of private profiles
- Follow platform Terms of Service

**Sources:**
- Artist websites (if mentioned in public art signage)
- Public art commission announcements
- Artist directories (CARFAC, Saskatchewan Arts Board)
- Gallery/studio websites
- LinkedIn (public profiles only)

**Tools:**
- Google search API
- LinkedIn public profile API (with appropriate authentication)
- Domain search for artist websites

**Output:**
```json
{
  "artist": "Artist Name",
  "contact_methods": [
    {"type": "website", "value": "https://...", "verified": true},
    {"type": "email", "value": "artist@...", "verified": false},
    {"type": "instagram", "value": "@username", "verified": true}
  ],
  "confidence": "high"
}
```

### Phase 3: Automated Outreach (High Risk - Requires Careful Design)

**Goal:** Contact artists for verification with minimal spam risk

**Ethical Requirements:**
- Opt-in only (artists must want to be contacted)
- Clear identification as automated outreach
- Easy opt-out mechanism
- Rate limiting (max 5 contacts per week initially)
- Personalized messages (not generic spam)
- Transparent about data usage

**Outreach Methods (Priority Order):**

1. **Website Contact Forms** (Preferred)
   - Most appropriate for automated outreach
   - Expected channel for project inquiries
   - Respects artist's chosen communication method

2. **Email** (If publicly listed on website/portfolio)
   - Professional and documented
   - Include unsubscribe mechanism
   - Use dedicated domain (e.g., artguide@jjacobsondesign.ca)

3. **Instagram DM** (Last resort, require manual approval)
   - Only if artist actively posts about public art
   - More personal, higher risk of being perceived as spam

**Message Template:**
```
Subject: Saskatoon Art Guide - Verify Your Public Artwork Entry

Hi [Artist Name],

I'm building the Saskatoon Art Guide, an open-source catalog of public
art in Saskatchewan. I came across your work "[Artwork Title]" at
[Location] and would like to include it with proper attribution.

Could you verify these details?
- Title: [Title]
- Year: [Year]
- Location: [Address]
- Medium: [Medium]

This is a public, non-commercial resource. You can view the project at:
https://github.com/Evakone/saskatoon-art-guide

If you'd like to provide additional information or corrections, please
reply to this message or submit via GitHub.

If you prefer NOT to be included, please let me know and I'll respect
that decision.

Best regards,
Josh Jacobson
Curator, Saskatoon Art Guide
https://www.jjacobsondesign.ca

---
This is an automated message. You received this because your artwork was
discovered in public records. To unsubscribe from future outreach, reply
with "UNSUBSCRIBE".
```

**Spam Prevention:**
- Maintain do-not-contact list
- Single contact per artist (no follow-ups without response)
- Clear sender identification
- Honest subject lines
- Opt-out mechanism in every message

### Phase 4: Response Processing (Medium Risk)

**Goal:** Process artist responses and update catalog

**Response Types:**

1. **Verification Confirmed** → Auto-add to staging file
2. **Corrections Needed** → Flag for manual review
3. **Opt-out Request** → Add to do-not-contact list, remove entry
4. **No Response** → Mark as unverified, don't publish

**Workflow:**
```
1. Email response received
2. Parse response (GPT-4 for natural language understanding)
3. Extract corrections/confirmations
4. Update staging file: data/staged/pending_verification.json
5. Curator approves batch weekly
6. Approved entries → saskatoon.json
```

### Phase 5: Integration with GitHub (Low Risk)

**Goal:** Automate PR creation for curator approval

**Process:**
1. Staged entries reach threshold (e.g., 10 artworks)
2. GitHub Action creates branch: `automated-submission-YYYYMMDD`
3. Adds entries to `saskatoon.json`
4. Opens PR with summary:
   - Number of entries
   - Artist verification status
   - Source links
5. Curator reviews and merges

**GitHub Action Triggers:**
- Weekly schedule
- Manual trigger via workflow dispatch
- When staging file exceeds threshold

## Implementation Roadmap

### Month 1: Foundation
- [ ] Set up discovery scripts for 2-3 reliable sources
- [ ] Create `data/discovered/` structure
- [ ] Build confidence scoring system
- [ ] Manual testing with 10-20 artworks

### Month 2: Contact Discovery
- [ ] Implement artist contact finder
- [ ] Build contact verification system
- [ ] Create do-not-contact list
- [ ] Test with 5 artists manually

### Month 3: Outreach System
- [ ] Set up dedicated email address
- [ ] Build outreach template system
- [ ] Implement rate limiting
- [ ] Create unsubscribe mechanism
- [ ] **Manual approval required for first 50 contacts**

### Month 4: Response Processing
- [ ] Email parsing system
- [ ] Natural language understanding for responses
- [ ] Staging file automation
- [ ] Weekly batch review workflow

### Month 5: GitHub Integration
- [ ] GitHub Action for PR creation
- [ ] Automated testing
- [ ] Monitoring and logging

### Month 6: Scaling
- [ ] Increase rate limits gradually
- [ ] Add more discovery sources
- [ ] Measure response rates
- [ ] Optimize based on feedback

## Technical Stack Recommendations

**Discovery & Processing:**
- Python 3.11+
- BeautifulSoup4 (web scraping)
- Pandas (data manipulation)
- OpenAI API / Claude API (contact info extraction, response parsing)

**Outreach:**
- SendGrid or AWS SES (email delivery)
- Gmail API (response monitoring)
- Dedicated email address with SPF/DKIM/DMARC configured

**Storage:**
- SQLite database for tracking contacts and responses
- CSV exports for curator review
- Git for final catalog updates

**Orchestration:**
- GitHub Actions (scheduled workflows)
- Cron jobs (for discovery scripts)
- Slack/Discord webhook for notifications

## Risk Mitigation

**Spam Risk:**
- Start with manual approval for all outreach
- Gradually automate as trust is established
- Monitor response rates (aim for >20% positive)
- Stop immediately if spam complaints occur

**Attribution Errors:**
- Never publish without artist verification or reliable source
- Maintain confidence scores for all fields
- Flag uncertain entries for manual review

**Privacy Concerns:**
- Only use publicly available information
- Respect opt-out requests immediately
- Don't store unnecessary personal data
- Be transparent about automation

**Reputation Risk:**
- Clear identification of automated process
- Professional communication
- Responsive to feedback
- Option for artists to request removal

## Success Metrics

**Discovery:**
- 50+ artworks discovered per month
- 80%+ accuracy on basic fields (title, artist, location)

**Outreach:**
- 20%+ response rate
- <1% spam complaints
- 50%+ verification rate

**Catalog Growth:**
- 10-20 verified entries per month
- 90%+ attribution accuracy
- Zero corrections needed post-publication

## Legal Considerations

- Consult with lawyer about automated outreach compliance
- Ensure CASL (Canadian Anti-Spam Legislation) compliance
- Privacy policy for contact information
- Terms of service for catalog usage

## Next Steps

1. Review this plan with trusted advisors/artists
2. Get feedback on outreach approach
3. Start with Phase 1 (Discovery) only
4. Pilot outreach with 5 artists manually
5. Iterate based on responses before automating
