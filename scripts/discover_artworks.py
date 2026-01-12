#!/usr/bin/env python3
"""
Saskatoon Art Guide - Discovery Script
Discovers public artworks from various sources and outputs to CSV
"""

import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse, quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run: pip install requests beautifulsoup4")
    exit(1)

# Configuration
OUTPUT_DIR = Path("data/discovered")
CANDIDATES_CSV = OUTPUT_DIR / "candidates.csv"
SOURCES_JSON = OUTPUT_DIR / "sources.json"
DISCOVERY_LOG = OUTPUT_DIR / "discovery.log"

# Rate limiting
REQUEST_DELAY = 1.0  # seconds between requests

class ArtworkCandidate:
    """Represents a discovered artwork with confidence scoring"""

    def __init__(self):
        self.title: str = ""
        self.artist: str = ""
        self.year: Optional[int] = None
        self.location: str = ""
        self.neighbourhood: str = ""
        self.medium: List[str] = []
        self.commissioned_by: str = ""
        self.source_url: str = ""
        self.source_name: str = ""
        self.confidence: str = "low"  # low, medium, high
        self.notes: str = ""
        self.discovered_at: str = datetime.now().isoformat()

    def calculate_confidence(self):
        """Calculate confidence score based on completeness"""
        score = 0
        if self.title: score += 1
        if self.artist: score += 2  # Artist is most important
        if self.year: score += 1
        if self.location: score += 1
        if self.source_url: score += 1

        if score >= 5:
            self.confidence = "high"
        elif score >= 3:
            self.confidence = "medium"
        else:
            self.confidence = "low"

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "artist": self.artist,
            "year": self.year,
            "location": self.location,
            "neighbourhood": self.neighbourhood,
            "medium": ", ".join(self.medium) if self.medium else "",
            "commissioned_by": self.commissioned_by,
            "source_url": self.source_url,
            "source_name": self.source_name,
            "confidence": self.confidence,
            "notes": self.notes,
            "discovered_at": self.discovered_at
        }


class DiscoveryEngine:
    """Main discovery engine for finding public art"""

    def __init__(self):
        self.candidates: List[ArtworkCandidate] = []
        self.sources: Dict[str, Dict] = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Saskatoon Art Guide Discovery Bot (Educational/Non-Commercial)'
        })

    def log(self, message: str):
        """Log to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(DISCOVERY_LOG, "a") as f:
            f.write(log_message + "\n")

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage with rate limiting"""
        try:
            self.log(f"Fetching: {url}")
            time.sleep(REQUEST_DELAY)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            self.log(f"Error fetching {url}: {e}")
            return None

    def extract_year(self, text: str) -> Optional[int]:
        """Extract year from text"""
        matches = re.findall(r'\b(19|20)\d{2}\b', text)
        if matches:
            year = int(matches[0])
            if 1900 <= year <= datetime.now().year:
                return year
        return None

    def _search_duckduckgo(self, query: str, max_results: int = 10) -> List[str]:
        """Search DuckDuckGo and return URLs"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            soup = self.fetch_page(url)
            if not soup:
                return []

            urls = []
            for link in soup.find_all('a', class_='result__url', href=True):
                href = link.get('href', '')
                # Skip DuckDuckGo internal links
                if href and not href.startswith('//duckduckgo.com'):
                    urls.append(href)
                    if len(urls) >= max_results:
                        break

            return urls
        except Exception as e:
            self.log(f"  Error searching: {e}")
            return []

    def discover_dtnyxe_blog(self):
        """Discover artworks from DTNYXE Downtown blog"""
        self.log("Starting DTNYXE blog discovery...")

        # Start with known article
        article_urls = set([
            "https://dtnyxe.ca/ness-jacobson-murals/",
        ])

        # Try to find more articles via site search using DuckDuckGo
        search_queries = [
            "site:dtnyxe.ca mural",
            "site:dtnyxe.ca public art",
            "site:dtnyxe.ca street art",
            "site:dtnyxe.ca artist",
        ]

        for query in search_queries:
            self.log(f"Searching for: {query}")
            urls = self._search_duckduckgo(query)
            article_urls.update(urls)
            time.sleep(REQUEST_DELAY)

        self.log(f"Found {len(article_urls)} DTNYXE articles to parse")

        # Parse each article
        for url in article_urls:
            soup = self.fetch_page(url)
            if not soup:
                continue
            self._parse_dtnyxe_article(url, soup)

        self.log(f"DTNYXE discovery complete. Found {len(self.candidates)} candidates so far.")

    def _parse_dtnyxe_article(self, url: str, soup: BeautifulSoup):
        """Parse a DTNYXE article for artwork information"""

        # Try to extract from meta tags first (more reliable for Elementor sites)
        meta_desc = soup.find('meta', {'name': 'description'}) or soup.find('meta', {'property': 'og:description'})
        meta_text = meta_desc.get('content', '') if meta_desc else ''

        # Extract article title and content
        title_elem = soup.find('h1') or soup.find('h2', class_='entry-title')

        # Try multiple content selectors for Elementor
        content = (
            soup.find('div', class_='entry-content') or
            soup.find('article') or
            soup.find('main') or
            soup.find('div', class_=lambda x: x and 'elementor-widget-container' in x)
        )

        # Combine meta text and content text
        text = meta_text
        if content:
            text += " " + content.get_text()

        if not text:
            self.log("  Could not find article content")
            return

        self.log(f"  Parsing article with {len(text)} characters")

        # Known artworks from this specific article
        known_artworks = [
            {
                "title": "Moving Forward",
                "artist": "Kent Ness",
                "location": "Dream's Building, Downtown Saskatoon, SK"
            },
            {
                "title": "Prairie Petals: Lilies in Luminous Frames",
                "artist": "Josh Jacobson",
                "location": "south-facing wall of Dream's building, Downtown Saskatoon, SK"
            }
        ]

        # For this specific DTNYXE article, we know the content
        if "ness-jacobson-murals" in url:
            for artwork in known_artworks:
                candidate = ArtworkCandidate()
                candidate.title = artwork["title"]
                candidate.artist = artwork["artist"]
                candidate.location = artwork["location"]
                candidate.neighbourhood = "Downtown"
                candidate.year = 2023  # Based on article date
                candidate.medium = ["paint"]
                candidate.commissioned_by = ""
                candidate.source_url = url
                candidate.source_name = "DTNYXE Downtown Blog"
                candidate.notes = "Extracted from: Ness + Jacobson collaborate on new downtown murals"
                candidate.calculate_confidence()

                if not self._is_duplicate(candidate):
                    self.candidates.append(candidate)
                    self.log(f"  Found: {candidate.artist} - {candidate.title}")

        # Also try generic extraction for other articles
        else:
            # Look for artist names (capitalized words)
            artist_patterns = [
                r'artist\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
                r'by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
                r'created by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            ]

            # Look for mural/artwork titles (quoted or after "titled")
            title_patterns = [
                r'"([^"]+)"',
                r'titled\s+([A-Z][^.]+)',
                r'mural\s+called\s+([A-Z][^.]+)',
            ]

            # Extract information
            artists = set()
            for pattern in artist_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                artists.update(matches)

            titles = set()
            for pattern in title_patterns:
                matches = re.findall(pattern, text)
                titles.update([m.strip() for m in matches if len(m.strip()) > 3])

            # Look for location mentions
            locations = re.findall(r'(?:at|on|located)\s+([^.]+(?:building|downtown|street|avenue))', text, re.IGNORECASE)

            year = self.extract_year(text)

            # If we found meaningful information, create candidates
            if artists and (titles or locations):
                for artist in artists:
                    candidate = ArtworkCandidate()
                    candidate.artist = artist
                    candidate.title = list(titles)[0] if titles else ""
                    candidate.location = list(locations)[0].strip() if locations else "Downtown Saskatoon, SK"
                    candidate.neighbourhood = "Downtown"
                    candidate.year = year
                    candidate.source_url = url
                    candidate.source_name = "DTNYXE Downtown Blog"
                    candidate.notes = "Extracted from blog article"

                    # Try to extract medium
                    if 'paint' in text.lower() or 'mural' in text.lower():
                        candidate.medium = ['paint']

                    candidate.calculate_confidence()

                    # Avoid duplicates
                    if not self._is_duplicate(candidate):
                        self.candidates.append(candidate)
                        self.log(f"  Found: {candidate.artist} - {candidate.title or 'Untitled'}")

    def discover_city_saskatoon(self):
        """Discover artworks from City of Saskatoon"""
        self.log("Starting City of Saskatoon discovery...")

        # Search for City of Saskatoon public art pages
        search_queries = [
            "site:saskatoon.ca public art",
            "site:saskatoon.ca mural",
            "saskatoon.ca outdoor art",
        ]

        city_urls = set()
        for query in search_queries:
            self.log(f"  Searching: {query}")
            urls = self._search_duckduckgo(query, max_results=5)
            city_urls.update(urls)
            time.sleep(REQUEST_DELAY)

        self.log(f"  Found {len(city_urls)} City of Saskatoon pages")

        for url in city_urls:
            soup = self.fetch_page(url)
            if soup:
                self._parse_generic_article(url, soup, "City of Saskatoon")

        self.log(f"City of Saskatoon discovery complete. Found {len(self.candidates)} candidates so far.")

    def discover_web_general(self):
        """Broad web search for Saskatoon murals and public art"""
        self.log("Starting general web discovery...")

        search_queries = [
            "Saskatoon mural artist",
            "Saskatoon public art downtown",
            "Saskatoon street art",
            "yxe mural",
            "Broadway Saskatoon art",
            "Riversdale Saskatoon mural",
        ]

        all_urls = set()
        for query in search_queries:
            self.log(f"  Searching: {query}")
            urls = self._search_duckduckgo(query, max_results=10)
            all_urls.update(urls)
            time.sleep(REQUEST_DELAY * 1.5)  # Extra delay for broader searches

        self.log(f"  Found {len(all_urls)} web pages about Saskatoon art")

        for url in all_urls:
            # Skip already processed domains
            if 'dtnyxe.ca' in url:
                continue

            soup = self.fetch_page(url)
            if soup:
                self._parse_generic_article(url, soup, "Web Search")

        self.log(f"General web discovery complete. Found {len(self.candidates)} candidates so far.")

    def discover_instagram_hashtags(self):
        """Note: Instagram requires authentication and API access"""
        self.log("Instagram discovery requires API credentials (skipped for now)")
        self.sources["instagram"] = {
            "status": "requires_api_access",
            "note": "Would search: #yxeart, #saskatoonart, #saskatoonmurals"
        }

    def _parse_generic_article(self, url: str, soup: BeautifulSoup, source_name: str):
        """Generic parser for any article about Saskatoon art"""

        # Extract all text
        text = soup.get_text()

        # Look for artist names (capitalized words)
        artist_patterns = [
            r'artist\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'created by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'painted by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        ]

        # Look for mural/artwork titles
        title_patterns = [
            r'"([^"]+)"',
            r'titled\s+"([^"]+)"',
            r'titled\s+([A-Z][^.,:;]+)',
            r'mural\s+called\s+"([^"]+)"',
            r'work\s+called\s+"([^"]+)"',
        ]

        # Extract information
        artists = set()
        for pattern in artist_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            # Filter out common false positives
            for match in matches:
                if match.lower() not in ['the city', 'city of', 'downtown saskatoon', 'the artist']:
                    artists.add(match)

        titles = set()
        for pattern in title_patterns:
            matches = re.findall(pattern, text)
            titles.update([m.strip() for m in matches if len(m.strip()) > 5 and len(m.strip()) < 100])

        # Look for Saskatoon locations
        location_patterns = [
            r'(?:at|on|located at)\s+([^.]+(?:building|downtown|street|avenue|broadway|riversdale|20th))',
            r'([^.]+(?:building|downtown|street|avenue|broadway|riversdale))\s+(?:in|at)\s+[Ss]askatoon',
        ]

        locations = set()
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            locations.update([m.strip() for m in matches if len(m.strip()) < 150])

        year = self.extract_year(text)

        # If we found meaningful information, create candidates
        if artists and (titles or locations):
            for artist in list(artists)[:10]:  # Limit to 10 artists per page
                candidate = ArtworkCandidate()
                candidate.artist = artist
                candidate.title = list(titles)[0] if titles else ""
                candidate.location = list(locations)[0] if locations else "Saskatoon, SK"
                candidate.neighbourhood = self._extract_neighbourhood(candidate.location)
                candidate.year = year
                candidate.source_url = url
                candidate.source_name = source_name
                candidate.notes = "Extracted via web search"

                # Try to extract medium
                if 'paint' in text.lower() or 'mural' in text.lower():
                    candidate.medium = ['paint']
                elif 'sculpture' in text.lower():
                    candidate.medium = ['sculpture']

                candidate.calculate_confidence()

                # Only add if decent confidence and not duplicate
                if candidate.confidence != "low" and not self._is_duplicate(candidate):
                    self.candidates.append(candidate)
                    self.log(f"  Found: {candidate.artist} - {candidate.title or candidate.location}")

    def _extract_neighbourhood(self, location: str) -> str:
        """Extract neighbourhood from location string"""
        location_lower = location.lower()
        if 'broadway' in location_lower:
            return "Broadway"
        elif 'riversdale' in location_lower:
            return "Riversdale"
        elif 'downtown' in location_lower:
            return "Downtown"
        elif '20th' in location_lower:
            return "Riversdale"
        else:
            return ""

    def _is_duplicate(self, candidate: ArtworkCandidate) -> bool:
        """Check if candidate is duplicate"""
        for existing in self.candidates:
            if (existing.artist == candidate.artist and
                existing.title == candidate.title):
                return True
        return False

    def export_candidates(self):
        """Export candidates to CSV"""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        with open(CANDIDATES_CSV, 'w', newline='', encoding='utf-8') as f:
            if self.candidates:
                fieldnames = list(self.candidates[0].to_dict().keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for candidate in self.candidates:
                    writer.writerow(candidate.to_dict())

        self.log(f"Exported {len(self.candidates)} candidates to {CANDIDATES_CSV}")

    def export_sources(self):
        """Export source information"""
        with open(SOURCES_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.sources, f, indent=2)

        self.log(f"Exported source information to {SOURCES_JSON}")

    def generate_report(self):
        """Generate discovery report"""
        report_path = OUTPUT_DIR / "discovery_report.md"

        high_conf = [c for c in self.candidates if c.confidence == "high"]
        medium_conf = [c for c in self.candidates if c.confidence == "medium"]
        low_conf = [c for c in self.candidates if c.confidence == "low"]

        report = f"""# Discovery Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- **Total Candidates**: {len(self.candidates)}
- **High Confidence**: {len(high_conf)}
- **Medium Confidence**: {len(medium_conf)}
- **Low Confidence**: {len(low_conf)}

## High Confidence Candidates

"""
        for candidate in high_conf:
            report += f"### {candidate.title or 'Untitled'}\n"
            report += f"- Artist: {candidate.artist}\n"
            report += f"- Location: {candidate.location}\n"
            report += f"- Year: {candidate.year or 'Unknown'}\n"
            report += f"- Source: [{candidate.source_name}]({candidate.source_url})\n\n"

        report += "\n## Next Steps\n\n"
        report += "1. Review high confidence candidates in `candidates.csv`\n"
        report += "2. Verify artist names and titles\n"
        report += "3. Confirm locations and commissioning information\n"
        report += "4. Add vetted entries to `data/artworks/saskatoon.json`\n"
        report += "5. Consider reaching out to artists for verification\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log(f"Generated report: {report_path}")

    def run_discovery(self):
        """Run full discovery pipeline"""
        self.log("=" * 60)
        self.log("Saskatoon Art Guide - Comprehensive Discovery Pipeline")
        self.log("=" * 60)

        # Run discovery from various sources
        self.discover_dtnyxe_blog()
        self.discover_city_saskatoon()
        self.discover_web_general()  # Broad web search
        self.discover_instagram_hashtags()

        # Export results
        self.export_candidates()
        self.export_sources()
        self.generate_report()

        self.log("=" * 60)
        self.log(f"Discovery complete! Found {len(self.candidates)} candidates.")
        self.log(f"Review results in: {OUTPUT_DIR}")
        self.log("=" * 60)


if __name__ == "__main__":
    engine = DiscoveryEngine()
    engine.run_discovery()
