import re
import requests
from typing import List, Dict
from urllib.parse import urlparse
import os

def parse_srt_file(source: str) -> List[Dict]:
    """
    Parses a local or remote .srt file into subtitle entries.
    Accepts either a local filepath or a URL.
    """
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source)
        content = response.text
    else:
        with open(source, 'r', encoding='utf-8') as file:
            content = file.read().strip()

    blocks = re.split(r'\n\s*\n', content)
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue

        time_line = lines[1]
        match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', time_line)
        if not match:
            continue

        start_time, end_time = match.groups()
        text = ' '.join(lines[2:]).strip()

        subtitles.append({
            "start": start_time,
            "end": end_time,
            "text": text
        })

    return subtitles


# --- Scene segmentation utilities ---
from datetime import datetime

def parse_srt_timestamp(ts: str) -> datetime:
    return datetime.strptime(ts, "%H:%M:%S,%f")

def segment_into_scenes(subs: List[Dict], min_gap_seconds: int = 4) -> List[Dict]:
    """
    Groups subtitle entries into scenes based on a time gap ≥ min_gap_seconds.
    Returns a list of scenes, each with start, end, and transcript.
    """
    scenes = []
    current_scene = []
    last_end_time = None

    for entry in subs:
        start = parse_srt_timestamp(entry["start"])
        end = parse_srt_timestamp(entry["end"])

        if last_end_time and (start - last_end_time).total_seconds() >= min_gap_seconds:
            if current_scene:
                scenes.append({
                    "start": current_scene[0]["start"],
                    "end": current_scene[-1]["end"],
                    "transcript": " ".join([s["text"] for s in current_scene])
                })
                current_scene = []

        current_scene.append(entry)
        last_end_time = end

    if current_scene:
        scenes.append({
            "start": current_scene[0]["start"],
            "end": current_scene[-1]["end"],
            "transcript": " ".join([s["text"] for s in current_scene])
        })

    return scenes