import json
from pathlib import Path

SAMPLE_RAW_PATH = Path("data/met_textile_objects_sample.json")
SAMPLE_OUTPUT_PATH = Path("data/met_formatted_data_sample.json")
RAW_PATH = Path("data/met_textile_objects.json")
OUTPUT_PATH = Path("data/met_formatted_data.json")
 
def format_objects(raw_data):
  formatted = []
  for obj in raw_data:
      id = obj.get("objectID")
      title = obj.get("title", "")
      objectName = obj.get("objectName", "")
      medium = obj.get("medium", "")
      culture = obj.get("culture", "")
      period = obj.get("period", "")
      dynasty = obj.get("dynasty") or ""
      reign = obj.get("reign") or ""
      objectDate = obj.get("objectDate", "")
      artistDisplayName = obj.get("artistDisplayName", "")
      artistDisplayBio = obj.get("artistDisplayBio", "")
      creditLine = obj.get("creditLine", "")
      classification = obj.get("classification", "")
      tags = ", ".join([tag.get("term", "") for tag in obj.get("tags", []) or []])

      embedding_text = (
          f"{title}, classified as a {objectName}. Made of {medium}, created around {objectDate} "
          f"during the {period} {dynasty} {reign}. Associated with {culture}. Classification: {classification}. "
          f"Created by {artistDisplayName} ({artistDisplayBio}). "
          f"Credit: {creditLine}. Tags: {tags}"
      )

      formatted.append({
          "id": id,
          "embedding_text": embedding_text,
          "image_url": obj.get("primaryImageSmall", ""),
          "raw": obj
      })

  return formatted

def main():
  # with open(SAMPLE_RAW_PATH, "r") as f:
  with open(RAW_PATH, "r") as f:
    raw_data = json.load(f)

    formatted_data = format_objects(raw_data)

  # with open(SAMPLE_OUTPUT_PATH, "w") as f:
  with open(OUTPUT_PATH, "w") as f:
    json.dump(formatted_data, f, indent=2)

    print(f"Formatted {len(formatted_data)} - {OUTPUT_PATH}")

if __name__ == "__main__":
  main()