import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import json
import re

def extract_json_block(response: str) -> dict:
    """
    Extracts the first JSON object from a messy LLM response using regex.
    Returns a parsed dict or an empty fallback.
    """
    try:
        match = re.search(r'\{.*?\}', response, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found")

        json_str = match.group(0)
        return json.loads(json_str)
    except Exception as e:
        print("Failed to parse LLM response:", e)
        print("Raw response:\n", response)
        return {
            "summary": "",
            "characters": [],
            "mood": "",
            "cultural_refs": []
        }

# Load the API token from .env
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HF_TOKEN:
    raise EnvironmentError("Missing HUGGINGFACEHUB_API_TOKEN in environment.")

# Initialize the Hugging Face client
client = InferenceClient(token=HF_TOKEN)

def analyze_scene(transcript: str, model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1") -> dict:
    """
    Sends the transcript to a Hugging Face LLM and returns structured annotations.
    """
    prompt = f"""
    You are a film scene analyst. Given the following transcript, return a JSON with:
    - "summary": One-sentence summary of the scene
    - "characters": List of mentioned characters
    - "mood": Mood or emotion of the scene
    - "cultural_refs": Up to 3 cultural references (or empty list if none)

    Transcript:
    {transcript}

    Output format:
    {{
      "summary": "...",
      "characters": [...],
      "mood": "...",
      "cultural_refs": [...]
    }}
    """

    response = client.text_generation(
        model=model,
        prompt=prompt.strip(),
        max_new_tokens=300,
        temperature=0.7
    )
    print("RAW LLM RESPONSE:\n", response)

    # NOTE: This assumes the model responds with valid Python-style dictionary
    return extract_json_block(response)