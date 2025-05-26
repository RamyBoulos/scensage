import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import json
import re
from .local_annotator import analyze_scene_locally
from .local_mistral import analyze_scene_with_mistral
from .utils import extract_json_block

# Load the API token from .env
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HF_TOKEN:
    raise EnvironmentError("Missing HUGGINGFACEHUB_API_TOKEN in environment.")

# Initialize the Hugging Face client
client = InferenceClient(token=HF_TOKEN)

def analyze_scene(transcript: str, model: str = None, llm_call=None, language: str = "English") -> dict:
    """
    Uses local model if USE_LOCAL is set to "mistral" (meaning local Mistral via Ollama), 
    otherwise falls back to Hugging Face API with the specified model (default "mistralai/Mistral-7B-Instruct-v0.1").
    Sends the transcript to an LLM and returns structured annotations.
    Accepts an optional llm_call function for mocking in tests.
    Retries once with a simplified prompt if parsing fails.
    """
    use_local = os.getenv("USE_LOCAL", "").lower()
    model = model or os.getenv("HF_MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.1")
    print("[DEBUG] use_local =", use_local)
    if use_local == "mistral":
        print("[INFO] Using local Mistral model via Ollama for inference.")
        return analyze_scene_with_mistral(transcript)

    print(f"[INFO] Using Hugging Face model: {model}")
    if not model or "mistral" not in model.lower():
        print(f"[WARNING] The specified model name '{model}' may not be correct or supported. Please verify the model name.")

    def build_prompt(t: str, language: str = "English") -> str:
        return f"""
You are a film scene analyst. Given the following transcript, respond with a **strict JSON object only** in {language} that includes:
- "summary": a one-sentence summary of the scene
- "characters": a list of mentioned characters (use real or generic names if unclear)
- "mood": the emotional tone of the scene (e.g. sad, tense, hopeful)
- "cultural_refs": up to 3 relevant cultural references or an empty list

Respond ONLY with valid JSON in {language}. Do NOT include explanations, markdown, or extra text.

Transcript:
{t}

Example response format:
{{
  "summary": "A narrator introduces the story.",
  "characters": ["Narrator"],
  "mood": "mysterious",
  "cultural_refs": []
}}
"""

    prompt = build_prompt(transcript, language=language)

    if llm_call:
        response = llm_call(prompt.strip())
    else:
        response = client.text_generation(
            model=model,
            prompt=prompt.strip(),
            max_new_tokens=200,
            temperature=0.7
        )

    print("RAW LLM RESPONSE:\n", response)
    parsed = extract_json_block(response)

    if not parsed["summary"]:
        # Retry with simplified prompt
        fallback_prompt = f"""
Return only valid JSON in {language} with:
- summary
- characters
- mood
- cultural_refs

Transcript:
{transcript}
"""

        if llm_call:
            response = llm_call(fallback_prompt.strip())
        else:
            response = client.text_generation(
                model=model,
                prompt=fallback_prompt.strip(),
                max_new_tokens=200,
                temperature=0.7
            )

        print("RETRY RAW LLM RESPONSE:\n", response)
        parsed = extract_json_block(response)

    if not parsed["summary"]:
        with open("annotation_errors.log", "a") as f:
            f.write("=== Failed Annotation ===\n")
            f.write(f"Transcript:\n{transcript}\n")
            f.write(f"Response:\n{response}\n\n")

    return parsed