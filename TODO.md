# TODO: Next Steps for Textile Pattern Recommender

This file outlines the remaining development steps for this project, including image embedding, vector storage, and building a user interface.

---

## ✅ Step 1: Dataset Collection and Curation

Completed and documented in `README.md`.

---

## Step 2: Image Embedding Strategy

Use a CLIP-based model (e.g., from `sentence-transformers`, `open-clip`, or `CLIP-as-service`) to generate image embeddings from museum objects.

### Pipeline:

1. **Extract image URLs**

   - **Cooper Hewitt:** Use the `z` size from the first image in the `images` array (height = 640px).
   - **The Met:** Use `primaryImageSmall` from the full object details.

2. **Download images temporarily (in memory)**

   - Use `requests.get()` or `PIL.Image.open(BytesIO(...))`
   - No need to save to disk

3. **Generate embeddings**

   - Load CLIP model (e.g., `CLIPProcessor` + `CLIPModel`, or `SentenceTransformer("clip-ViT-B-32")`)
   - Resize/preprocess images per model requirements
   - Get vector embeddings

4. **Store vector + metadata**

   - Format: `{ embedding: [...], id: ..., image_url: ..., text_fields: ..., metadata: ... }`
   - Save locally (JSON/Parquet) or to a vector DB (Chroma, Weaviate, Qdrant, etc.)

5. **Process user-uploaded image**

   - Same pipeline as above → generate embedding → search index

6. **Similarity search**
   - Cosine similarity or nearest neighbors to find matches

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
