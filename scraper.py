import os
import json
import re
import requests
from bs4 import BeautifulSoup

REPO_NAME = "IPAOMTK Self-Updating Mirror"
REPO_IDENTIFIER = "com.custom.ipaomtk.mirror"
BASE_URL = "https://ipaomtk.com"

def fetch_apps():
    apps_list = []
    # Advanced session headers mimicking a secure desktop browser environment
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    try:
        response = session.get(BASE_URL, timeout=15)
        if response.status_code != 200:
            return apps_list
            
        soup = BeautifulSoup(response.text, 'html.parser')
        # Target layout blocks likely holding app download page anchor points
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            if "/tag/" in href or "/category/" in href or href == f"{BASE_URL}/":
                continue
                
            # Match typical post layout patterns 
            if href.startswith(BASE_URL) and len(href) > len(BASE_URL) + 5:
                slug = href.replace(BASE_URL, "").strip("/")
                if "/" in slug or not slug:
                    continue
                    
                app_name = link.text.strip()
                if not app_name or len(app_name) < 3:
                    continue
                
                # Deduplicate elements
                if any(x['name'] == app_name for x in apps_list):
                    continue
                    
                download_url = f"https://file.ipaomtk.com/ipa/{slug}.ipa"
                
                apps_list.append({
                    "name": app_name,
                    "bundleIdentifier": f"com.ipaomtk.{slug.replace('-', '.')}",
                    "version": "1.0",
                    "versionDate": "2026-06-30",
                    "downloadURL": download_url,
                    "iconURL": "https://ipaomtk.com/favicon.ico",
                    "size": 0,
                    "category": "Tweaked",
                    "developerName": "IPAOMTK"
                })
    except Exception as e:
        print(f"Scraper encountered a soft error: {e}")
        
    return apps_list

def main():
    print("Executing deep parsing pass...")
    scraped_apps = fetch_apps()
    
    # Fallback list preserves your working entries if Cloudflare blocks the script entirely
    if len(scraped_apps) == 0:
        print("Crawl yielded zero public records due to network protection. Preserving baseline items.")
        scraped_apps = [
            {
                "name": "AI ARTA: Art & Photo Generator",
                "bundleIdentifier": "com.aiby.aiart",
                "version": "2.8",
                "versionDate": "2026-06-30",
                "downloadURL": "https://file.ipaomtk.com/ipa/AI-Arta.ipa",
                "iconURL": "https://ipaomtk.com/favicon.ico",
                "size": 5950900,
                "category": "AI",
                "developerName": "Aiby"
            },
            {
                "name": "CarX Street",
                "bundleIdentifier": "com.carxtech.sr",
                "version": "1.0",
                "versionDate": "2026-06-30",
                "downloadURL": "https://file.ipaomtk.com/ipa/carx-street.ipa",
                "iconURL": "https://ipaomtk.com/favicon.ico",
                "size": 0,
                "category": "Games",
                "developerName": "CarX"
            }
        ]
        
    repo_structure = {
        "name": REPO_NAME,
        "identifier": REPO_IDENTIFIER,
        "apps": scraped_apps
    }
    
    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_structure, f, indent=2, ensure_ascii=False)
    print(f"Sync execution finalized. Total available catalog definitions mapped: {len(scraped_apps)}")

if __name__ == "__main__":
    main()
