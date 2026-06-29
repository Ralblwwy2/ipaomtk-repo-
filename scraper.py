import os
import json
import re
import requests

REPO_NAME = "IPAOMTK Self-Updating Mirror"
REPO_IDENTIFIER = "com.custom.ipaomtk.mirror"

def fetch_live_library():
    apps_list = []
    # Using their direct high-volume data feed endpoint that bypasses front-end firewalls
    api_url = "https://ipaomtk.com/wp-json/wp/v2/posts"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    # Requesting 100 entries per page to collect their full library map
    params = {
        'per_page': 100,
        '_fields': 'title,slug'
    }
    
    try:
        print("Connecting directly to official IPAOMTK data streams...")
        response = requests.get(api_url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            posts = response.json()
            print(f"Connection verified! Parsing {len(posts)} verified items...")
            
            for post in posts:
                raw_title = post.get("title", {}).get("rendered", "")
                slug = post.get("slug", "")
                
                if not raw_title or not slug:
                    continue
                
                # Dynamic version parsing regex: Extracts accurate release numbers from titles (e.g., v1.2, version 19.4)
                version_match = re.search(r'(?:v|version\s?)(\d+\.\d+[\.\d+]*)', raw_title, re.IGNORECASE)
                real_version = version_match.group(1) if version_match else "1.0"
                
                # Format a clean app name by separating the version text tags safely
                display_name = re.sub(r'(?:v|version\s?)(\d+\.\d+[\.\d+]*).*', '', raw_title, flags=re.IGNORECASE).strip()
                display_name = display_name.replace("&#8211;", "-").replace("&amp;", "&")
                
                download_url = f"https://file.ipaomtk.com/ipa/{slug}.ipa"
                
                apps_list.append({
                    "name": display_name if display_name else raw_title,
                    "bundleIdentifier": f"com.ipaomtk.{slug.replace('-', '.')}",
                    "version": real_version,
                    "versionDate": "2026-06-30",
                    "downloadURL": download_url,
                    "iconURL": "https://ipaomtk.com/favicon.ico",
                    "size": 0,
                    "category": "Tweaked",
                    "developerName": "IPAOMTK"
                })
        else:
            print(f"API rejection error. Server state code: {response.status_code}")
            
    except Exception as network_err:
        print(f"Connection timeout tracking error: {network_err}")
        
    return apps_list

def main():
    scraped_apps = fetch_live_library()
    
    # Absolute structural backup so the repository code never clears if the server drops frames
    if not scraped_apps:
        print("Data extraction failed. Script exited cleanly without wiping target file.")
        return

    repo_structure = {
        "name": REPO_NAME,
        "identifier": REPO_IDENTIFIER,
        "apps": scraped_apps
    }
    
    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_structure, f, indent=2, ensure_ascii=False)
    print(f"Build phase successful! Populated repo.json with {len(scraped_apps)} up-to-date items.")

if __name__ == "__main__":
    main()
