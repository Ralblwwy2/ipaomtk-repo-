import os
import json
import requests

REPO_NAME = "IPAOMTK Self-Updating Mirror"
REPO_IDENTIFIER = "com.custom.ipaomtk.mirror"

def main():
    print("Initializing fallback data map...")
    
    # Pre-compiled working static routes from their library 
    # This prevents Cloudflare blocking your automation completely
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
    print("Database definition maps written out successfully to repo.json!")

if __name__ == "__main__":
    main()
