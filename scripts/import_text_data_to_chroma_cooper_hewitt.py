import json
from pathlib import Path
import chromadb

CHROMA_DIR = "chroma_db"
client = chromadb.PersistentClient(path=CHROMA_DIR)

COLLECTION_NAME = "cooper_hewitt_text_objects"
collection = client.get_or_create_collection(name=COLLECTION_NAME)

BATCH_DIR = Path("data/cooper_hewitt_text_embeddings")
batch_files = sorted(BATCH_DIR.glob("*.json"))

for file in batch_files:
  print(f"Processing {file.name}")
  with open(file) as f:
    batch = json.load(f)

    if not batch:
      continue

    ids = [str(obj["id"]) for obj in batch]
    embeddings = [obj["embeddings"] for obj in batch]
    documents = [obj["text_fields"] for obj in batch]
    metadatas = [obj["metadata"] | {"image_url": obj["image_url"]} for obj in batch]

    collection.upsert(
      ids=ids,
      embeddings=embeddings,
      documents=documents,
      metadatas=metadatas
    )

print(f"Indexed {len(batch_files)} batch files into ChromaDB")