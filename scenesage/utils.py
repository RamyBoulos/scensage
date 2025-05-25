from datetime import datetime
import json
import re

def parse_srt_timestamp(ts: str) -> datetime:
    """Parse an SRT timestamp string into a datetime object."""
    return datetime.strptime(ts, "%H:%M:%S,%f")


# Utility function to extract JSON from a messy LLM response

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
