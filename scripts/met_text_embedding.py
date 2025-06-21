import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

DATA_PATH = Path("data/met_formatted_data.json")
OUTPUT_DIR = Path("data/met_text_embeddings")
OUTPUT_DIR.mkdir(exist_ok=True)

with open("data/met_formatted_data.json") as f:
  data = json.load(f)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

batch_size = 50
total = len(data)

for start_index in range(0, total, batch_size):
  end_index = min(start_index + batch_size, total)
  batch = data[start_index:end_index]
  results = []

  for obj in batch:
    text_fields = obj.get("embedding_text", "")
    embedding = model.encode(text_fields).tolist()

    results.append({
      "id": obj["id"],
      "image_url": obj["image_url"],
      "embeddings": embedding,
      "text_fields": text_fields,
      "metadata": {
        "title": obj["raw"].get("title", ""),
        "medium": obj["raw"].get("medium", ""),
        "date": obj["raw"].get("date", ""),
        "description": obj["raw"].get("description", "")
      }
    })

  batch_num = start_index // batch_size
  filename = OUTPUT_DIR / f"met_text_embeddings_batch_{batch_num}.json"

  with open(filename, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)