import os
import json
import requests

REPO_NAME = "IPAOMTK Self-Updating Mirror"
REPO_IDENTIFIER = "com.custom.ipaomtk.mirror"

# We are pulling from an open, community-maintained database feed 
# that already bypassed the restrictions and indexed thousands of tweaked IPAs
COMMUNITY_DATA_FEED = "https://swaggyp36000.github.io/TrollStore-IPAs/apps.json"

def main():
    print("Connecting to open database feed...")
    try:
        response = requests.get(COMMUNITY_DATA_FEED, timeout=15)
        if response.status_code != 200:
            print("Failed to fetch community index.")
            return

        source_data = response.json()
        raw_apps = source_data.get("apps", [])
        
        print(f"Successfully retrieved index. Processing {len(raw_apps)} applications...")
        
        # Format the fetched apps to perfectly match your repo schema
        processed_apps = []
        for app in raw_apps:
            processed_apps.append({
                "name": app.get("name", "Unknown Application"),
                "bundleIdentifier": app.get("bundleIdentifier", "com.custom.app"),
                "version": app.get("version", "1.0"),
                "versionDate": app.get("versionDate", "2026-06-30"),
                "downloadURL": app.get("downloadURL", ""),
                "iconURL": app.get("iconURL", "https://ipaomtk.com/favicon.ico"),
                "size": app.get("size", 0),
                "category": app.get("category", "Tweaked"),
                "developerName": app.get("developerName", "Community")
            })

        repo_structure = {
            "name": REPO_NAME,
            "identifier": REPO_IDENTIFIER,
            "apps": processed_apps
        }

        with open("repo.json", "w", encoding="utf-8") as f:
            json.dump(repo_structure, f, indent=2, ensure_ascii=False)
        print(f"Successfully populated repo.json with {len(processed_apps)} apps completely automatically!")

    except Exception as e:
        print(f"Critical error during sync pass: {e}")

if __name__ == "__main__":
    main()
