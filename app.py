import gradio as gr
import numpy as np
import clip
import torch
from PIL import Image
from sentence_transformers import SentenceTransformer
import chromadb
from torchvision import transforms

preview_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.CenterCrop(224),
])

client = chromadb.PersistentClient(path="chroma_db")
# I ended up not using the text collections in this as the image collections provided better similarity
met_text_collection = client.get_collection("met_text_objects")
cooper_hewitt_text_collection = client.get_collection("cooper_hewitt_text_objects")
met_image_collection = client.get_collection("met_objects")
cooper_hewitt_image_collection = client.get_collection("cooper_hewitt_objects")

device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_clip_text_embedding(text_prompt: str):
    # Tokenize the input text for CLIP
    tokens = clip.tokenize([text_prompt]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(tokens)
    return text_features[0].cpu().tolist()

def handle_chat(prompt: str, history) -> str:
    query_embedding = get_clip_text_embedding(prompt)

    met_results = met_image_collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["metadatas", "distances", "documents"]
    )

    cooper_hewitt_results = cooper_hewitt_image_collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["metadatas", "distances", "documents"]
    )

    combined = []
 
    output = "## Textile Suggestions Based on Your Prompt:\n"

    for object, distance in zip(
        met_results["metadatas"][0],
        met_results["distances"][0]
    ):
        combined.append((1 - distance, object))
    for object, distance in zip(
        cooper_hewitt_results["metadatas"][0],
        cooper_hewitt_results["distances"][0]        
    ):
        combined.append((1 - distance, object))
    combined.sort(reverse=True, key=lambda x: x[0])  # sort by similarity
    for score, obj in combined[:5]:
        title = obj["title"]
        image_url = obj.get("image_url", "")
        description = obj.get("description", "")
        object_url = obj.get("object_url", "")
        medium = obj.get("medium")
        output += f"### {title}: _Similarity Score: {score:.2f}_\n"
        if image_url:
            output += f"![{title}]({image_url})\n"
        if medium:
            output += f"**Medium:** {medium}\n\n"
        if description:
            output += f"**Description:** {description}\n\n"
        if object_url:
            output += f'<a href="{object_url}" target="_blank" rel="noopener noreferrer">View museum object</a>\n'

    return output.strip()

def get_similar(input_img):
    if isinstance(input_img, np.ndarray):
        input_img = Image.fromarray(input_img.astype('uint8'))
    image_input = preprocess(input_img).unsqueeze(0).to(device)    
    preview_img = preview_transform(input_img)
    with torch.no_grad():
        image_features = model.encode_image(image_input)

    embedding_vector = image_features[0].cpu().tolist()

    met_results = met_image_collection.query(
        query_embeddings=[embedding_vector],
        n_results=5,
        include=["metadatas", "distances", "documents"]
    )

    cooper_hewitt_results = cooper_hewitt_image_collection.query(
        query_embeddings=[embedding_vector],
        n_results=5,
        include=["metadatas", "distances", "documents"]
    )

    combined = []

    output = "## Textile Suggestions Based on Your Prompt:\n"

    for object, distance in zip(
        met_results["metadatas"][0],
        met_results["distances"][0]
    ):
        combined.append((1 - distance, object))

    for object, distance in zip(
        cooper_hewitt_results["metadatas"][0],
        cooper_hewitt_results["distances"][0]
    ):
        combined.append((1 - distance, object))
       
    combined.sort(reverse=True, key=lambda x: x[0])  # sort by similarity
    for score, obj in combined[:5]:
        title = obj["title"]
        image_url = obj.get("image_url", "")
        description = obj.get("description", "")
        object_url = obj.get("object_url", "")
        medium = obj.get("medium")
        output += f"### {title}: _Similarity Score: {score:.2f}_\n"
        if image_url:
            output += f"![{title}]({image_url})\n"
        if medium:
            output += f"**Medium:** {medium}\n\n"
        if description:
            output += f"**Description:** {description}\n\n"
        if object_url:
            output += f'<a href="{object_url}" target="_blank" rel="noopener noreferrer">View museum object</a>\n'

    return preview_img, output.strip()

with gr.Blocks(title="Textile Pattern Recommender") as demo:
    gr.Markdown("# Textile Pattern Recommender")

    with gr.Tabs():
        with gr.TabItem("Text Prompt"):
            gr.ChatInterface(fn=handle_chat)

        with gr.TabItem("Image Upload"):
            gr.Interface(
                fn=get_similar,
                inputs=gr.Image(label="Upload an Image", type="pil"),
                outputs=[gr.Image(label="Preprocessed Image"), gr.Markdown()],
                title="Image-Based Search"
            )

demo.launch()

if __name__ == "__main__":
    demo.launch()