from scenesage.parser import parse_srt_file, segment_into_scenes

def test_parsed_subtitles_are_nonempty():
    subs = parse_srt_file("tests/data/plan9.srt")
    assert isinstance(subs, list)
    assert len(subs) > 0
    assert all("start" in sub and "end" in sub and "text" in sub for sub in subs)

def test_scene_segmentation_multiple_scenes():
    subs = parse_srt_file("tests/data/plan9.srt")
    scenes = segment_into_scenes(subs)
    assert isinstance(scenes, list)
    assert len(scenes) > 1  # We expect multiple scenes based on pauses in this file
    assert all("start" in s and "end" in s and "transcript" in s for s in scenes)


# Mock LLM segmenter: groups every 5 subtitles as one "scene"
def mock_llm_segmenter(subs):
    # Mock: group every 5 subtitles as one "scene"
    scenes = []
    for i in range(0, len(subs), 5):
        chunk = subs[i:i+5]
        scenes.append({
            "start": chunk[0]["start"],
            "end": chunk[-1]["end"],
            "transcript": " ".join([s["text"] for s in chunk])
        })
    return scenes


def test_scene_segmentation_llm_mode():
    subs = parse_srt_file("tests/data/plan9.srt")
    scenes = segment_into_scenes(subs, mode="llm", llm_segmenter=mock_llm_segmenter)
    assert isinstance(scenes, list)
    assert len(scenes) > 0
    assert all("start" in s and "end" in s and "transcript" in s for s in scenes)


def test_scene_segmentation_gap_vs_llm():
    subs = parse_srt_file("tests/data/plan9.srt")
    scenes_gap = segment_into_scenes(subs, mode="gap")
    scenes_llm = segment_into_scenes(subs, mode="llm", llm_segmenter=mock_llm_segmenter)
    assert isinstance(scenes_gap, list)
    assert isinstance(scenes_llm, list)
    assert scenes_gap != scenes_llm  # Expect different grouping logic