import json
from pathlib import Path

# Load a small sample dataset to verify things are working
sample_path = Path("data/met_textile_objects_sample.json")

if sample_path.exists():
    with open(sample_path, "r") as f:
        sample_data = json.load(f)
    print(f"Loaded {len(sample_data)} sample Cooper Hewitt objects.")
else:
    print("No sample data found. Please run a data script or check the path.")

# Future: image/text embedding, vector store setup, retrieval logic, UI