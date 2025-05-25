import requests
import json
import os

def get_ollama_host():
    # Priority: OLLAMA_HOST env var > /.dockerenv presence > localhost
    ollama_host = os.getenv("OLLAMA_HOST")
    if ollama_host:
        return ollama_host
    # Detect if running inside Docker
    if os.path.exists('/.dockerenv'):
        return "host.docker.internal"
    return "localhost"

OLLAMA_HOST = get_ollama_host()
OLLAMA_URL = f"http://{OLLAMA_HOST}:11434"

def is_ollama_running() -> bool:
    try:
        r = requests.get(OLLAMA_URL)
        return r.status_code == 200
    except Exception:
        return False

def analyze_scene_with_mistral(transcript: str) -> dict:
    """
    Uses Ollama's local API to analyze a scene using the quantized mistral model.
    Returns a structured JSON object or fallback values.
    """
    prompt = f"""
    You are a film scene analyst. Analyze the following scene and return only a valid JSON object with the following keys:
    "summary", "characters", "mood", "cultural_refs".
    Your response must start with '{{' and end with '}}'. Do not include explanations, formatting, or markdown.

    Scene:
    {transcript}
    """

    try:
        if not is_ollama_running():
            print(f"[ERROR] Ollama server is not running on {OLLAMA_URL}")
            return {
                "summary": "",
                "characters": [],
                "mood": "",
                "cultural_refs": []
            }
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt.strip(),
                "stream": False
            },
            timeout=60
        )
        result = response.json().get("response", "").strip()
        print("RAW MISTRAL RESPONSE:\n", result)

        # Try to parse as JSON
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # Try to wrap and parse
            if not result.startswith("{"):
                result = "{" + result
            if not result.endswith("}"):
                result += "}"
            return json.loads(result)

    except Exception as e:
        print("Failed to get or parse response from Mistral:", e)
        return {
            "summary": "",
            "characters": [],
            "mood": "",
            "cultural_refs": []
        }

# Test block
if __name__ == "__main__":
    print(f"[DEBUG] Using Ollama at {OLLAMA_URL}")
    test_input = "A man lights a cigarette as he walks down a quiet street under neon lights."
    output = analyze_scene_with_mistral(test_input)
    print(json.dumps(output, indent=2))