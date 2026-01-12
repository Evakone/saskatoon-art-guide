#!/usr/bin/env python3
"""
Saskatoon Art Guide - Contact Finder
Finds public contact information for artists discovered in the catalog
"""

import csv
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run: pip install requests beautifulsoup4")
    exit(1)

# Configuration
DATA_DIR = Path("data/discovered")
CANDIDATES_CSV = DATA_DIR / "candidates.csv"
CONTACTS_JSON = DATA_DIR / "contacts.json"

# Rate limiting
REQUEST_DELAY = 2.0  # Be respectful with search engines

class ArtistContact:
    """Represents contact information for an artist"""

    def __init__(self, name: str):
        self.name = name
        self.website: Optional[str] = None
        self.instagram: Optional[str] = None
        self.email: Optional[str] = None
        self.public_profiles: List[str] = []
        self.confidence: str = "low"
        self.notes: str = ""

    def calculate_confidence(self):
        """Calculate confidence based on number of verified contacts"""
        score = 0
        if self.website: score += 2
        if self.instagram: score += 1
        if self.email: score += 1
        if self.public_profiles: score += 1

        if score >= 3:
            self.confidence = "high"
        elif score >= 2:
            self.confidence = "medium"
        else:
            self.confidence = "low"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "website": self.website,
            "instagram": self.instagram,
            "email": self.email,
            "public_profiles": self.public_profiles,
            "confidence": self.confidence,
            "notes": self.notes
        }


class ContactFinder:
    """Finds public contact information for artists"""

    def __init__(self):
        self.contacts: Dict[str, ArtistContact] = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36'
        })

    def log(self, message: str):
        """Log message"""
        print(f"[ContactFinder] {message}")

    def search_artist(self, artist_name: str) -> ArtistContact:
        """Search for artist contact information"""
        self.log(f"Searching for: {artist_name}")

        contact = ArtistContact(artist_name)

        # Try to find website
        website = self._find_website(artist_name)
        if website:
            contact.website = website
            self.log(f"  Found website: {website}")

        # Try to find Instagram
        instagram = self._find_instagram(artist_name)
        if instagram:
            contact.instagram = instagram
            self.log(f"  Found Instagram: {instagram}")

        # Search for public profiles
        profiles = self._find_public_profiles(artist_name)
        contact.public_profiles = profiles

        contact.calculate_confidence()
        return contact

    def _find_website(self, artist_name: str) -> Optional[str]:
        """Search for artist website using Google"""
        try:
            # Simple DuckDuckGo HTML search (doesn't require API)
            query = f"{artist_name} artist saskatoon website"
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

            time.sleep(REQUEST_DELAY)
            response = self.session.get(url, timeout=10)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for results that might be artist websites
            for link in soup.find_all('a', class_='result__url'):
                href = link.get('href', '')
                # Filter for likely artist websites
                if any(term in href.lower() for term in ['art', 'design', 'portfolio', artist_name.lower().replace(' ', '')]):
                    # Clean up the URL
                    if href.startswith('//duckduckgo.com/l/?'):
                        continue
                    return href

        except Exception as e:
            self.log(f"  Error searching for website: {e}")

        return None

    def _find_instagram(self, artist_name: str) -> Optional[str]:
        """Try to find Instagram profile"""
        # Check common patterns
        username_variants = [
            artist_name.lower().replace(' ', ''),
            artist_name.lower().replace(' ', '_'),
            artist_name.lower().replace(' ', '.'),
        ]

        for username in username_variants:
            # We can't actually verify without API, but we can suggest
            self.log(f"  Possible Instagram: @{username}")

        return None  # Requires API access or manual verification

    def _find_public_profiles(self, artist_name: str) -> List[str]:
        """Find other public profiles (LinkedIn, CARFAC, etc.)"""
        profiles = []

        # Known artist directories
        directories = [
            "https://www.carfac.ca",
            "https://saskculture.ca",
            "https://www.saskartsboard.ca",
        ]

        # This would require actual scraping of each directory
        # For now, just note them as potential sources
        self.log(f"  Check artist directories manually for {artist_name}")

        return profiles

    def process_candidates(self):
        """Process all candidates from CSV"""
        if not CANDIDATES_CSV.exists():
            self.log(f"No candidates file found at {CANDIDATES_CSV}")
            return

        with open(CANDIDATES_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            artists = set()

            for row in reader:
                artist = row.get('artist', '').strip()
                if artist and artist not in artists:
                    artists.add(artist)

        self.log(f"Found {len(artists)} unique artists to research")

        for artist in artists:
            if artist not in self.contacts:
                contact = self.search_artist(artist)
                self.contacts[artist] = contact
                time.sleep(REQUEST_DELAY)  # Be respectful

    def export_contacts(self):
        """Export contact information to JSON"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        contacts_dict = {
            name: contact.to_dict()
            for name, contact in self.contacts.items()
        }

        with open(CONTACTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(contacts_dict, f, indent=2)

        self.log(f"Exported {len(self.contacts)} artist contacts to {CONTACTS_JSON}")

    def generate_summary(self):
        """Generate summary of contact findings"""
        high_conf = [c for c in self.contacts.values() if c.confidence == "high"]
        medium_conf = [c for c in self.contacts.values() if c.confidence == "medium"]
        low_conf = [c for c in self.contacts.values() if c.confidence == "low"]

        print("\n" + "=" * 60)
        print("Contact Discovery Summary")
        print("=" * 60)
        print(f"Total Artists: {len(self.contacts)}")
        print(f"High Confidence: {len(high_conf)}")
        print(f"Medium Confidence: {len(medium_conf)}")
        print(f"Low Confidence: {len(low_conf)}")
        print("\nHigh Confidence Contacts:")
        for contact in high_conf:
            print(f"  - {contact.name}")
            if contact.website:
                print(f"    Website: {contact.website}")
            if contact.instagram:
                print(f"    Instagram: {contact.instagram}")
        print("=" * 60)

    def run(self):
        """Run contact finder pipeline"""
        self.log("Starting contact discovery...")
        self.process_candidates()
        self.export_contacts()
        self.generate_summary()
        self.log("Contact discovery complete!")


if __name__ == "__main__":
    finder = ContactFinder()
    finder.run()
