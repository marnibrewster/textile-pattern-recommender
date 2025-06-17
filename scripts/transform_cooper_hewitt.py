import json
from pathlib import Path

SAMPLE_RAW_PATH = Path("data/cooper_hewitt_textile_objects_sample.json")
SAMPLE_OUTPUT_PATH = Path("data/cooper_hewitt_formatted_data_sample.json")
RAW_PATH = Path("data/cooper_hewitt_textile_objects.json")
OUTPUT_PATH = Path("data/cooper_hewitt_formatted_data.json")
 
def format_objects(raw_data):
  formatted = []

  for obj in raw_data:
      id = obj.get("id")

      title = obj.get("title", "")
      description = obj.get("description", "")
      label_text = obj.get("label_text") or obj.get("gallery_text") or ""
      medium = obj.get("medium", "")
      object_type = obj.get("type", "")
      date = obj.get("date", "")
      creditline = obj.get("creditline", "")
      country = obj.get("woe:country_name", "")
      url = obj.get("url", "")

      # Participants (e.g., designers, weavers)
      participants = obj.get("participants", [])
      creators = ", ".join([
          f"{p.get('person_name', '')} ({p.get('role_display_name', '')})"
          for p in participants if p.get('person_name') and p.get('role_display_name')
      ])

      # Construct embedding text
      embedding_text = (
          f"{title}. {description} {label_text}. Made of {medium}. "
          f"{object_type}, {date}. Designed or created by {creators}. "
          f"From {country}. Credit: {creditline}."
      )

      # Get image URL from the 'z' size
      image_url = ""
      if obj.get("images"):
          image_dict = obj["images"][0]
          image_url = image_dict.get("z", {}).get("url", "")

      formatted.append({
          "id": id,
          "embedding_text": embedding_text,
          "image_url": image_url,
          "url": url,
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