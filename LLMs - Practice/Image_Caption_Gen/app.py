# import os
# import gradio as gr
# import google.generativeai as genai
# from PIL import Image

# # ✅ Load API key directly from environment variable
# api_key = os.getenv("api_key")
# print(api_key)

# if not api_key:
#     raise ValueError("❌ GEMINI_API_KEY not found in environment variables.")

# genai.configure(api_key=api_key)

# # ✅ Use model that supports image input
# model = genai.GenerativeModel("models/gemini-2.5-flash-image")

# def generate_caption(image):
#     if image is None:
#         return "Please upload an image first."
#     try:
#         img = Image.open(image)
#         prompt = "Describe this image in one short, meaningful sentence."
#         response = model.generate_content([prompt, img])
#         return response.text or "No caption generated."
#     except Exception as e:
#         return f"Error: {str(e)}"

# # ✅ Gradio UI
# interface = gr.Interface(
#     fn=generate_caption,
#     inputs=gr.Image(type="filepath", label="Upload an Image"),
#     outputs="text",
#     title="🖼️ AI Image Caption Generator",
#     description="Upload an image and get an automatically generated caption using Gemini 2.5 Vision."
# )

# if __name__ == "__main__":
#     interface.launch()



import os
import gradio as gr
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Gemini Vision model
GEMINI_MODEL = "gemini-2.5-flash-image"

# Hugging Face fallback model (offline)
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
fallback_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def generate_caption(image):
    if image is None:
        return "Please upload an image first."

    try:
        # Try Gemini Vision API first
        img = Image.open(image)
        prompt = "Act like a professional social media manager. Generate a highly creative, catchy caption for this image."
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content([prompt, img])
        return response.text or "No caption generated."

    except Exception as e:
        # Fallback: Use Hugging Face BLIP model with creativity tuning
        print(f"⚠️ Gemini failed, switching to Hugging Face model. Error: {e}")
        raw_image = Image.open(image).convert('RGB')
        inputs = processor(raw_image, return_tensors="pt").to(device)

        # 🧠 Add sampling params for creativity
        out = fallback_model.generate(
            **inputs,
            max_new_tokens=50,      # longer captions
            temperature=1,          # increase creativity
            top_p=0.9,              # nucleus sampling
            do_sample=True          # enable random sampling
        )

        caption = processor.decode(out[0], skip_special_tokens=True)
        return f"(🎨) {caption}"

# Gradio UI
interface = gr.Interface(
    fn=generate_caption,
    inputs=gr.Image(type="filepath", label="Upload an Image"),
    outputs="text",
    title="🖼️ AI Image Caption Generator",
    description="Uploads an image and generates a creative caption using Gemini Vision, with a Hugging Face fallback."
)

if __name__ == "__main__":
    interface.launch()
