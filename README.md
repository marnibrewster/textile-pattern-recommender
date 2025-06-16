# 🧵 Textile Pattern Recommender

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

## 📚 Data Sources

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

### Potential future sources that I might use:

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

## Step 1: Data Pipeline: From Raw to Indexed

### Start with Raw API Data

_Note: This project uses large datasets sourced from public APIs. To keep the repository lightweight and within GitHub storage limits, full raw and processed JSON files are not included._

Instead, a few small sample files (e.g., `data/sample_cooper_hewitt_objects.json`) are provided to illustrate the data structure and format used.

If you'd like to generate the full datasets yourself, follow the steps in the code in the scripts directory (e.g., `scripts/get_ch_data.py` and `scripts/get_met_data.py`). For the Cooper Hewitt API, you'll need a `COOPER_ACCESS_TOKEN` which can be created after you [create an API key](https://collection.cooperhewitt.org/api).

### Cooper Hewitt

The initial textile data is fetched from the [Cooper Hewitt API](https://collection.cooperhewitt.org/api) in `scripts/get_ch_data.py` and saved as `data/cooper_hewitt_textile_objects.json`. We will use `query=textile&has_images=1&has_no_known_copyright=0`.

**Filter objects:** We have to filter these out in `scripts/get_ch_data.py` as the API doesn't support negation

- the word "sample" in the string value of the following keys: `title` or `type` (sample books and swatches are typically used for testing techniques or displaying material options rather than being finished textile works - we want to focus on complete, intentional textile designs)

**Text for embedding:**

- title
- description
- gallery_text or label_text (they're usually similar — pick one)
- medium
- type (e.g., Blanket, Curtain, Sampler)
- creditline (can hint at cultural/historical origin)
- participants[].person_name + participants[].role_display_name
- date (optional — can help suggest era or style)

ex: `embedding_text = f"{title}. {description} {label_text}. Made of {medium}. {type}, {date}. Designed by {maker}."`

**For metadata (keep raw):**

- accession_number (unique ID)
- date, decade
- medium
- type
- dimensions or dimensions_raw
- woe:country_name (geographic/cultural origin)
- image_urls (pick one size, e.g., 640px)
- participants (for attribution)
- url (to the museum object page)

**We can omit the values from the following keys:**

- year_acquired, tms:id, markings, signed, inscribed, has_no_known_copyright, on_display, is_loan_object,
- Raw `images` dict beyond preferred size

### The Met

First we perform a search for `objectIDs` by querying the [The Metropolitan Museum of Art Collection API](https://metmuseum.github.io/) using this endpoint `https://collectionapi.metmuseum.org/public/collection/v1/search?medium=textiles&hasImages=true&q=a` to find all textile objects that have associated images. The results are fetched in `scripts/get_met_data.py` and saved as `data/textile_objectIDs.json`.

Note: We use `q=a` because we can't use "." and we can't filter the objects endpoint with `hasImages` or `medium`. Using "a" as the search term almost guarantees that we get accurate results, as we have to assume that almost every object contains the character "a".

This returns a JSON response containing an array of objectIDs for all textile objects that have associated images. We save these IDs to `data/textile_objectIDs.json` (see `data/textile_object_IDs_sample.json`) to use for fetching the full object details in the next step.

Then for each objectID in raw*met_objectIDs, fetch the full object details including images from the Met's object endpoint using `scripts/get_met_data.py`. \_Note that we use a `time.sleep` as the Met only allows 80 requests per second.*

This returns detailed object information including image URLs under:

- `primaryImage`: Full resolution image
- `primaryImageSmall`: Smaller resolution image (recommended)

The full object details are saved to `data/met_textile_objects.json` for further processing (see `data/met_textile_objects_sample.json`). This file contains the complete metadata and image information for each textile object that matched our search criteria. We'll use this raw data as input for the filtering and processing steps described above.

**Text for embedding:**

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

Ex: `embedding_text = f"{title}, classified as a {objectName}. Made of {medium}, created around {objectDate} during the {period} period. Associated with {culture}. Created by {artistDisplayName} ({artistDisplayBio}). Credit: {creditLine}. Tags: {tags}"`

**We can omit the values from the following keys:**

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

### See TODO.md for next steps
