# TODO: Next Steps for Textile Pattern Recommender

This file outlines the remaining development steps for this project, including image embedding, vector storage, and building a user interface.

---

## ✅ Step 1: Dataset Collection and Curation

Completed and documented in `README.md`.

## ✅ Step 2a: Image Embedding Strategy

Completed and documented in `README.md`.

---

## Step 2b: Text Embedding Strategy

Completed and documented in `README.md`.

---

## Step 3: Vector Database Setup and Query Logic

Completed and documented in `README.md`.

---

## Step 4: Create User Interface

Completed and documented in `README.md`.

---

## Possible UI enhancement:

### Option B: **Next.js + FastAPI**

- Frontend: Next.js (supports image uploads, slick UX)
- Backend: FastAPI (handles embedding + search)
- Scalable and customizable

Features to include:

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
