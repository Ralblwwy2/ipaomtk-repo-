import os
import json
import requests

REPO_NAME = "IPAOMTK Self-Updating Mirror"
REPO_IDENTIFIER = "com.custom.ipaomtk.mirror"

# Direct hidden API endpoint used by the IPAOMTK site platform to supply app lists
IPAOMTK_API = "https://ipaomtk.com/wp-json/wp/v2/posts?per_page=100&_fields=title,slug,excerpt"

def fetch_live_data():
    apps_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }
    
    try:
        # Fetching directly via the WordPress REST API endpoint which usually bypasses front-end browser firewall blocks
        response = requests.get(IPAOMTK_API, headers=headers, timeout=15)
        if response.status_code == 200:
            posts = response.json()
            print(f"API Connection Successful! Found {len(posts)} dynamic entries.")
            
            for post in posts:
                # Extract clean string data from API mapping
                raw_title = post.get("title", {}).get("rendered", "")
                slug = post.get("slug", "")
                
                if not raw_title or not slug:
                    continue
                
                # Dynamic version parser: extracts real version flags (e.g., 1.5.2) out of the title string safely
                import re
                version = "1.0"
                version_match = re.search(r'(?:v|v\s?|version\s?)(\d+\.\d+[\.\d+]*)', raw_title, re.IGNORECASE)
                if version_match:
                    version = version_match.group(1)
                
                # Clean the version flags out of the display name so it looks professional
                clean_name = re.sub(r'(?:v|v\s?|version\s?)(\d+\.\d+[\.\d+]*).*', '', raw_title, flags=re.IGNORECASE).strip()
                clean_name = clean_name.replace("&#8211;", "-").replace("&amp;", "&")
                
                download_url = f"https://file.ipaomtk.com/ipa/{slug}.ipa"
                
                apps_list.append({
                    "name": clean_name if clean_name else raw_title,
                    "bundleIdentifier": f"com.ipaomtk.{slug.replace('-', '.')}",
                    "version": version,
                    "versionDate": "2026-06-30",
                    "downloadURL": download_url,
                    "iconURL": "https://ipaomtk.com/favicon.ico",
                    "size": 0,
                    "category": "Tweaked",
                    "developerName": "IPAOMTK"
                })
        else:
            print(f"API server responded with code: {response.status_code}")
    except Exception as e:
        print(f"API read error: {e}")
        
    return apps_list

def main():
    print("Initiating direct API sync database crawl...")
    scraped_apps = fetch_live_data()
    
    # Safety fallback preserves your 34 apps layout if the live API blocks the runner
    if not scraped_apps:
        print("API blocked by host security framework. Retaining hardcoded baseline index.")
        return
        
    repo_structure = {
        "name": REPO_NAME,
        "identifier": REPO_IDENTIFIER,
        "apps": scraped_apps
    }
    
    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_structure, f, indent=2, ensure_ascii=False)
    print(f"Database generation complete. Successfully compiled {len(scraped_apps)} dynamic live records.")

if __name__ == "__main__":
    main()
