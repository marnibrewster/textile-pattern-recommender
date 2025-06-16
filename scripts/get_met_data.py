import json
from pathlib import Path
import time
import requests

OBJECT_IDS_PATH = Path("data/textile_objectIDs.json")
OUTPUT_PATH = Path("data/met_textile_objects.json")

def get_textile_object(objectID):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed on object ID {objectID}: {response.status_code}")
        return []

def main():
    all_objects = []

    with open(OBJECT_IDS_PATH, "r") as f:
        objectIDs = json.load(f)

    for objectID in objectIDs:
        print(f"Fetching object ID {objectID} ...")
        object_data = get_textile_object(objectID)
        if not object_data:
            continue
        all_objects.append(object_data)
        time.sleep(0.03)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_objects, f, indent=2)
    print(f"Saved {len(all_objects)} objects to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
