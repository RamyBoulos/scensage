from scenesage.annotator import analyze_scene

def mock_llm_call(prompt: str) -> str:
    return """
    {
      "summary": "The narrator warns the audience about strange future events.",
      "characters": ["narrator"],
      "mood": "dramatic",
      "cultural_refs": ["War of the Worlds"]
    }
    """

def test_analyze_scene_with_mock_llm():
    scene = {
        "start": "00:00:00,000",
        "end": "00:00:05,000",
        "transcript": "Strange events are coming. Can your heart take it?"
    }

    annotated = analyze_scene(scene, llm_call=mock_llm_call)

    assert annotated["summary"]
    assert "narrator" in annotated["characters"]
    assert annotated["mood"] == "dramatic"
    assert isinstance(annotated["cultural_refs"], list)