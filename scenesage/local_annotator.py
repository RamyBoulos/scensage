import requests

def analyze_scene_locally(transcript: str, language: str = "English") -> dict:
    prompt = f"""
    Summarize this scene and extract structured details in JSON format. Respond in {language} only.

    Transcript:
    {transcript}

    Respond in the format:
    {{
        "summary": "...",
        "characters": [...],
        "mood": "...",
        "cultural_refs": []
    }}
    """

    try:
        import os
        ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        print(f"[DEBUG] Using Ollama host: {ollama_host}")
        response = requests.post(
            f"http://{ollama_host}:11434/api/generate",
            json={"model": "mistral", "prompt": prompt.strip(), "stream": False},
            timeout=60
        )
        result = response.json()["response"]
    except Exception as e:
        print("Error during local model inference:", e)
        result = ""

    try:
        import json
        parsed = json.loads(result)
        return parsed
    except Exception as e:
        print("Failed to parse model output as JSON.")
        print("Raw output:", result)
        return {
            "summary": "",
            "characters": [],
            "mood": "",
            "cultural_refs": []
        }

# Test block
if __name__ == "__main__":
    test_scene = "John and Sarah argue about their future while packing boxes in a small apartment."
    output = analyze_scene_locally(test_scene)
    print("Model Output:\n", output)