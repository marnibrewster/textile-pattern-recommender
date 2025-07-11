# Textile Pattern Recommender

⚠️ **Work In Progress**

This is an active personal project under development. Code, data handling, and model integration are still evolving. Expect updates, bugs, and unfinished components. Feedback and collaboration welcome!

This project is a non-commercial, educational exploration that helps users find visually or thematically similar historical textile patterns based on an image upload, theme keyword, or mood description. The code and models are used solely for research and learning purposes, with all rights to the textile images and metadata remaining with their respective owners.

Inputs:

- image upload OR
- natural language prompt (example: "botanical blues", "sacred geometry", "bold shapes")

Outputs:

- Suggested historical patterns (images and metadata)
- Info: origin, date, material, use case, design notes
- Optional: similar stitches/fabrics/colors or exportable inspiration board

Why this isn't "just ChatGPT":

- Visual matching (image -> embedding)
- Semantic tagging + metadata filtering
- Curated dataset of textile history (which ChatGPT doesn't have embedded)
- Custom UX and retrieval logic

Note: This is a portfolio project, not a fully open-source tool intended for general reuse. Scripts are included to demonstrate my process, but full reproduction requires access tokens and substantial local data processing. If you’re curious about implementation details, see the code and comments.

## Data Sources

This project draws from two major museum and cultural institution APIs to build a diverse dataset of textile patterns:

### Cooper Hewitt Museum

- Primary source for this project
- Rich metadata including materials, techniques, dimensions
- High-quality images with multiple resolutions
- Well-documented API with comprehensive documentation

### Metropolitan Museum of Art

- Over 30,000 textile objects in public domain
- Detailed provenance and cultural context
- Open Access API with CC0 license
- Includes historical textiles from multiple cultures

<details>
<summary>Potential future sources that I might use:</summary>

#### Victoria & Albert Museum

- World's largest museum collection of decorative arts
- Specialized textile and fashion collections
- API provides access to digitized collection
- Strong focus on pattern design and techniques

#### Europeana Collections

- Aggregates content from European institutions
- Multiple textile-related collections
- Standardized metadata across sources
- APIs for searching and retrieving records

#### The Quilt Index

- Specialized database of historical quilts
- Detailed pattern and technique documentation
- Focus on American quilting traditions
- Research-oriented metadata schema
- Con: no API!

#### Smithsonian Institution

- Multiple museums with textile holdings
- Comprehensive API across collections
- High-resolution image availability
- Detailed conservation information
- Con: possible overlap with Cooper Hewitt, lack of uniform structure, lack of images, copyright murkiness

</details>

## Step 1: Data Pipeline: From Raw to Indexed

### Start with Raw API Data

_Note: This project uses large datasets sourced from public APIs. To keep the repository lightweight and within GitHub storage limits, full raw and processed JSON files are not included._

Instead, a few small sample files (e.g., [sample data objects json](data/sample_cooper_hewitt_objects.json)) are provided to illustrate the data structure and format used.

If you'd like to generate the full datasets yourself, follow the steps in the code in the scripts directory (e.g., [scripts/get_ch_data.py](scripts/get_ch_data.py) and [scripts/get_met_data.py](scripts/get_met_data.py)). For the Cooper Hewitt API, you'll need a `COOPER_ACCESS_TOKEN` which can be created after you [create an API key](https://collection.cooperhewitt.org/api). To run [scripts/get_ch_data.py](scripts/get_ch_data.py), you'll need to create an `.env` file at the root of the project. Copy the contents of [sample.env](sample.env) and paste it into `.env`, then paste your api access token directly after the "=".

### Cooper Hewitt

The initial textile data is fetched from the [Cooper Hewitt API](https://collection.cooperhewitt.org/api) in [scripts/get_ch_data.py](scripts/get_ch_data.py) and saved as [data/cooper_hewitt_textile_objects.json](data/cooper_hewitt_textile_objects.json). We will use `query=textile&has_images=1&has_no_known_copyright=0`.

**Filter objects:** We have to filter these out in [scripts/get_ch_data.py](scripts/get_ch_data.py) as the API doesn't support negation

- the word "sample" in the string value of the following keys: `title` or `type` (sample books and swatches are typically used for testing techniques or displaying material options rather than being finished textile works - we want to focus on complete, intentional textile designs)

<details>
<summary><b>Text for embedding:</b></summary>

- title
- description
- gallery_text or label_text (they're usually similar — pick one)
- medium
- type (e.g., Blanket, Curtain, Sampler)
- creditline (can hint at cultural/historical origin)
- participants[].person_name + participants[].role_display_name
- date (optional — can help suggest era or style)
</details>

ex: `embedding_text = f"{title}. {description} {label_text}. Made of {medium}. {type}, {date}. Designed by {maker}."`

<details>
<summary><b>For metadata (keep raw):</b></summary>

- `accession_number (unique ID)`
- `date, decade`
- `medium`
- `type`
- `dimensions or dimensions_raw`
- `woe:country_name (geographic/cultural origin)`
- `image_urls (pick one size, e.g., 640px)`
- `participants (for attribution)`
- `url (to the museum object page)`
</details>

<details>
<summary><b>Keys we can omit:</b></summary>

- `year_acquired`, `tms:id`, `markings`, `signed`, `inscribed`, `has_no_known_copyright`, `on_display`, `is_loan_object`,
- Raw `images` dict beyond preferred size

</details>

### The Met

First we perform a search for `objectIDs` by querying the [The Metropolitan Museum of Art Collection API](https://metmuseum.github.io/) using this endpoint `https://collectionapi.metmuseum.org/public/collection/v1/search?medium=textiles&hasImages=true&q=a` to find all textile objects that have associated images. The results are fetched in [scripts/get_met_data.py](scripts/get_met_data.py) and saved as [data/textile_objectIDs.json](data/textile_objectIDs.json).

Note: We use `q=a` because we can't use "." and we can't filter the objects endpoint with `hasImages` or `medium`. Using "a" as the search term almost guarantees that we get accurate results, as we have to assume that almost every object contains the character "a".

This returns a JSON response containing an array of objectIDs for all textile objects that have associated images. We save these IDs to [data/textile_objectIDs.json](data/textile_objectIDs.json) (see [sample json](data/textile_object_IDs_sample.json)) to use for fetching the full object details in the next step.

Then for each objectID in raw*met_objectIDs, fetch the full object details including images from the Met's object endpoint using [scripts/get_met_data.py](scripts/get_met_data.py). \_Note that we use a `time.sleep` as the Met only allows 80 requests per second.*

This returns detailed object information including image URLs under:

- `primaryImage`: Full resolution image
- `primaryImageSmall`: Smaller resolution image (recommended)

The full object details are saved to [data/met_textile_objects.json](data/met_textile_objects.json) for further processing (see [sample json](data/met_textile_objects_sample.json)). This file contains the complete metadata and image information for each textile object that matched our search criteria. We'll use this raw data as input for the filtering and processing steps described above.

<details>
<summary><b>Text for embedding:</b></summary>

- `title`
- `objectName`
- `medium`
- `culture`
- `period`
- `dynasty (if not null)`
- `reign (if not null)`
- `objectDate`
- `artistDisplayName`
- `artistDisplayBio`
- `creditLine`
- `classification`
- `tags[].term`

</details>

Ex: `embedding_text = f"{title}, classified as a {objectName}. Made of {medium}, created around {objectDate} during the {period} period. Associated with {culture}. Created by {artistDisplayName} ({artistDisplayBio}). Credit: {creditLine}. Tags: {tags}"`

<details>

<summary><b>Keys we can omit:</b></summary>

- `artistAlphaSort`
- `artistPrefix`
- `artistSuffix`
- `artistGender`
- `artistWikidata_URL`
- `artistULAN_URL`
- `objectWikidata_URL`
- `metadataDate`
- `repository`
- `GalleryNumber`
- `rightsAndReproduction`
- `dimensionsParsed`
- `measurements`
- `locale, locus, subregion, region, excavation, river`
- `linkResource (duplicate of objectURL)`
</details>

## Step 2a: Image Embedding Strategy

Use a CLIP-based model to generate image embeddings from museum objects. This step was performed in [Google Colab](https://colab.research.google.com/) to take advantage of free / low-cost GPUT resources and avoid long runtimes on my local machine.

### Why Google Colab?

- Free access to GPUs (I used `ViT-B/32` via `openai/CLIP`)
- Easy to test batching and monitor results
- Avoided large local memory and compute usage
- All results downloaded as `.json` batch files per 50-object chunk

### Pipeline:

1. **Extract image URLs** (_Handled during our transformation step:_)

   - **Cooper Hewitt:** Use the `z` size from the first image in the `images` array (height = 640px).
   - **The Met:** Use `primaryImageSmall` from the full object details, and updated the [scripts/transform_met.py](scripts/transform_met.py) script and re-ran it to exclude objects without a `primaryImageSmall`.

2. **Download images temporarily (in memory)**

   - Use `requests.get()` with `PIL.Image.open(BytesIO(...))`
   - No image files were saved to disk

3. **Generate embeddings in batches** ([see notebook for code](notebooks/image_embedding_demo.ipynb))

   - Load CLIP model (`ViT-B/32` via `clip` package)
   - Preprocessed images with `clip.load(...)[1]
   - Ran embedding extraction on batches of 50 objects
   - Captured failed image URLs in a CSV log for later reprocessing

     [See example data](data/met_embeddings_batch_0_sample.json)

4. **Store vector + metadata**

Each batch output contained objects in the following format:

```
{
  "id": "object_id",
  "image_url": "https://...",
  "embedding": [...],
  "text_fields": "long description used for text search",
  "metadata": {
    "title": "...",
    "medium": "...",
    "date": "...",
    "description": "...",
    "object_url": "https://..."
  }
}
```

- Saved locally as JSON in batch files like:
- See [batch sample data](data/cooper_hewitt_embeddings_batch_0_sample.json)

## Step 2b: Text Embedding Strategy

We’ve now generated text embeddings for both The Met and Cooper Hewitt datasets and stored them in separate ChromaDB collections.

### Pipeline

1. Transform structured object metadata into natural language text.

   - During the [transform_met](scripts/transform_met.py) and [transform_cooper_hewitt](scripts/transform_cooper_hewitt.py) scripts, we created a embedding_text field combining title, medium, culture, period, and other available fields into a readable sentence.

2. Generate sentence embeddings.

- We used the all-MiniLM-L6-v2 model from sentence-transformers.

- Embeddings were generated in batches of 50 and saved to disk (e.g., data/met_text_embeddings/met_text_embeddings_batch_0.json).

3. Store vector + metadata.

- Format:

```
{
"id": "...",
"image_url": "...",
"embedding": [...],
"metadata": {
  "title": "...",
  "medium": "...",
  "date": "...",
  "description": "..."
}
}
```

These JSON batch files are used to populate the Chroma vector database.

4. Insert into ChromaDB.

- Two collections created for text embeddings with `import_text_data_to_chroma` scripts:

  - met_text_objects

  - cooper_hewitt_text_objects

  These live alongside the image-based collections (met_objects, cooper_hewitt_objects).

Sample Files:

For transparency, a few example text embedding files are available in data/sample_batches/:

[data/sample_batches/met_text_embeddings_batch_0_sample.json](data/sample_batches/met_text_embeddings_batch_0_sample.json)

[data/sample_batches/cooper_hewitt_text_embeddings_batch_0_sample.json](data/sample_batches/cooper_hewitt_text_embeddings_batch_0_sample.json)

Note: Full embedding datasets are excluded from version control. See .gitignore for excluded paths.

## Step 3: Vector Database Setup and Query Logic

### Embedded Image and Text Data Using CLIP

All museum object data (from The Met and Cooper Hewitt) was embedded using CLIP's `ViT-B/32` model. This included both the image and the associated metadata (title, medium, description, etc.).

### Unified Vector DB for All Queries

After evaluating weak performance using standalone text embeddings (all-MiniLM-L6-v2), we switched to using the CLIP text encoder for text prompts as well. This allowed both image and text queries to use the image-based vector databases, which contain richer embeddings.

### ChromaDB Re-indexing with Cosine Similarity

To support CLIP's cosine similarity space, the image collections were re-indexed with:

`metadata={"hnsw:space": "cosine"}`

This ensures accurate similarity scoring during retrieval.

### Dual-Source Querying

For both text and image input, the app queries the image vector databases:

- `met_objects`

- `cooper_hewitt_objects`

  The top 5 results from each are merged and sorted by similarity score before being returned to the user.

## Step 4: User Interface with Gradio

Created a tabbable user interface that allows the user to use a text prompt or an image prompt to return similar items.

### TODO:

See [TODO.md](TODO.md) for next steps

#### Notebooks

[Embedding script run in Google Colab](notebooks/image_embedding_demo.ipynb)  
 ![screenshot](./assets/clip_demo_output.png)
