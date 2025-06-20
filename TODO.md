# TODO: Next Steps for Textile Pattern Recommender

This file outlines the remaining development steps for this project, including image embedding, vector storage, and building a user interface.

---

## ✅ Step 1: Dataset Collection and Curation

Completed and documented in `README.md`.

## ✅ Step 2a: Image Embedding Strategy

Completed and documented in `README.md`.

---

## Step 2b: Text Embedding Strategy

We generate text embeddings from curated metadata fields (like title, description, material, culture, artist, etc.) using a sentence-transformer model such as `sentence-transformers/all-MiniLM-L6-v2` or a similar lightweight encoder.

Each object is processed to produce a combined text string that captures key semantic information (see the scripst [scripts/transform_met.py](scripts/transform_met.py) and [scripts/transform_cooper_hewitt.py](scripts/transform_cooper_hewitt.py), and check out an example of the data they output: [data/met_formatted_data_sample.json](data/met_formatted_data_sample.json) and [data/cooper_hewitt_formatted_data_sample.json](data/cooper_hewitt_formatted_data_sample.json)). Each entry in these files includes:

- A synthesized `embedding_text`
- Key metadata (`id`, `image_url`, and the full object in `raw`)

We then generate embeddings and store them in a vector database.

These vectors are used to support similarity search based on natural language queries, such as "sacred geometry" or "botanical blues." Text embeddings and image embeddings are stored alongside each object's metadata for multi-modal retrieval.

---

## Step 3: Create User Interface

Decide between:

### Option A: **Gradio prototype**

- Simple UI for image upload and text input
- Great for fast demos and testing
- Minimal deployment effort

### Option B: **Next.js + FastAPI**

- Frontend: Next.js (supports image uploads, slick UX)
- Backend: FastAPI (handles embedding + search)
- Scalable and customizable

Features to include:

- Upload or prompt-based search
- Display image matches with metadata
- Optional: pin matches to a board / export
- Optional: filters by era, origin, medium, etc.

---

## Optional Enhancements

- [ ] Add text-based embedding (e.g., using same CLIP model for descriptions)
- [ ] Create hybrid search (text + image)
- [ ] Cluster results by style or region
- [ ] Export to Pinterest board / moodboard builder
- [ ] Add logging for model confidence
- [ ] Compare embeddings across institutions

---

## Notes

- Cooper Hewitt API requires a personal access token
- Large data files are excluded from the repo (see `README.md`)
- Sample objects are available in `data/` for testing
