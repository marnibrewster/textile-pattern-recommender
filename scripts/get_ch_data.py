import json
from pathlib import Path
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("COOPER_ACCESS_TOKEN")

OUTPUT_PATH = Path("data/cooper_hewitt_textile_objects.json")
PER_PAGE = 100
MAX_PAGES = 50  # Adjust as needed

def get_textile_objects(page_num):
    url = f"https://api.collection.cooperhewitt.org/rest/?method=cooperhewitt.search.objects&access_token={ACCESS_TOKEN}&query=textile&has_images=1&per_page={PER_PAGE}&page={page_num}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("objects", [])
    else:
        print(f"Failed on page {page_num}: {response.status_code}")
        return []

def filter_sample_objects(objects):
    return [
        obj for obj in objects
        if "sample" not in obj.get("title", "").lower()
        and "sample" not in obj.get("type", "").lower()
    ]

def main():
    all_filtered = []

    for page in range(1, MAX_PAGES + 1):
        print(f"Fetching page {page}...")
        raw = get_textile_objects(page)
        if not raw:
            break  # Stop if no more data
        filtered = filter_sample_objects(raw)
        all_filtered.extend(filtered)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_filtered, f, indent=2)
    print(f"Saved {len(all_filtered)} filtered objects to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
