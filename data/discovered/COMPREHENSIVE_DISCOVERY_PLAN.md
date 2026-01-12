# Comprehensive Discovery - What's Different This Time

## The Problem With First Run

You were right - I only looked at ONE article we already knew about. That found exactly what was already in the catalog (2 artworks, 2 artists). Not helpful.

## What's Running Now (Overnight)

This comprehensive discovery searches **multiple sources across the web** to find NEW artworks you don't have:

### 1. DTNYXE Blog (Expanded)
**Search Queries:**
- `site:dtnyxe.ca mural`
- `site:dtnyxe.ca public art`
- `site:dtnyxe.ca street art`
- `site:dtnyxe.ca artist`

**Expected Results:** 10-20 DTNYXE articles about art projects

### 2. City of Saskatoon
**Search Queries:**
- `site:saskatoon.ca public art`
- `site:saskatoon.ca mural`
- `saskatoon.ca outdoor art`

**Expected Results:** 3-5 official city pages about public art programs

### 3. General Web Search (NEW)
**Search Queries:**
- `Saskatoon mural artist`
- `Saskatoon public art downtown`
- `Saskatoon street art`
- `yxe mural`
- `Broadway Saskatoon art`
- `Riversdale Saskatoon mural`

**Expected Results:** 30-60 web pages including:
- Local news articles (StarPhoenix, CBC Saskatchewan)
- Artist portfolios and websites
- Business listings mentioning murals
- Tourism and culture blogs
- Community announcements
- Gallery and festival pages

## What Makes This Better

### More Sources
- 13 different search queries (vs. 1 article before)
- 50-100 web pages analyzed (vs. 1 before)
- Multiple domains and perspectives

### Better Extraction
- Generic article parser handles any site structure
- Improved artist name detection
- Better location extraction (neighbourhoods)
- Filters false positives
- Medium/high confidence only

### Expected Discoveries
- **Realistic:** 10-20 new artworks
- **Optimistic:** 30-50 new artworks
- **Best case:** 50-100 new artworks

Each with:
- Artist name
- Title (when available)
- Location (neighbourhood when possible)
- Year (when mentioned)
- Source URL for verification
- Confidence score

## Runtime

- **First run:** ~13 seconds (1 article, 2 artworks)
- **This run:** ~5-10 minutes (50-100 pages, 10-100 artworks)

Worth the wait for real discoveries!

## What You'll Review Tomorrow

```
data/discovered/
├── candidates.csv              # All discovered artworks
├── discovery_report.md         # Organized by confidence
├── contacts.json               # Artist websites/profiles
└── discovery.log               # Full execution details
```

### Review Workflow

1. **Start with high-confidence candidates** (most complete data)
2. **Check source URLs** (verify the information)
3. **Research missing fields** (commissioning, exact location)
4. **Add vetted entries** to saskatoon.json
5. **Consider outreach** to artists for verification

## Sources This Will Find

- Downtown Saskatoon BID projects
- Riversdale Business Improvement District art
- Saskatchewan Arts Board funded works
- Broadway BID commissions
- Individual artist portfolios
- News coverage of unveilings
- Business websites featuring murals
- Tourism Saskatoon features
- University of Saskatchewan campus art
- Private commissions mentioned publicly

## Quality Controls

- Duplicate detection (won't re-add existing works)
- False positive filtering (ignores "The City", "The Artist", etc.)
- Confidence scoring (only medium/high exported)
- Source attribution (every discovery has URL)
- Rate limiting (respects robots.txt)

## After This Run

You can:
1. **Review and add** the discoveries to your catalog
2. **Identify patterns** (which artists are prolific, which neighbourhoods)
3. **Prioritize outreach** (contact high-confidence artists first)
4. **Refine searches** (add more queries for underrepresented areas)
5. **Schedule weekly** (set up cron job for continuous discovery)

---

**Status:** Running comprehensive discovery now...
**Check back in 5-10 minutes for results!**
