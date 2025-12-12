# Visionary Captioner — AI Image Caption Generator

## Overview
Visionary Captioner is a simple web app that generates descriptive captions for images using AI models (Gemini). It provides an easy Gradio UI, optional MongoDB saving, and multiple caption modes (short, detailed, creative).

## Requirements
- Python 3.10+
- Gemini API key (from Google AI Studio)
- (Optional) MongoDB URI (Atlas)
- Libraries: see `requirements.txt`

## Setup
1. Clone or create the project folder.
2. Copy `.env.example` to `.env` and fill in your `GEMINI_API_KEY` and optionally `MONGO_URI`.
3. Install dependencies:
