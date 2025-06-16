import json
from pathlib import Path
import requests

OUTPUT_PATH = Path("data/textile_objectIDs.json")

def get_textile_objectIDs():
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?medium=Textiles&hasImages=true&q=a"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("objectIDs", [])
    else:
        print(f"Failed: {response.status_code}")
        return []

def main(): 
    raw = get_textile_objectIDs()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(raw, f, indent=2)
    print(f"Saved {len(raw)} filtered objects to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
