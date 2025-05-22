from parser import parse_srt_file, segment_into_scenes
from annotator import analyze_scene

url = "https://commons.wikimedia.org/wiki/TimedText:Plan_9_from_Outer_Space_(1959).webm.en.srt"
subs = parse_srt_file(url)

print("First 10 subtitle entries:")
for sub in subs[:10]:
    print(sub)

print("\nFirst 2 scenes after segmentation and annotation:\n" + "-"*40)
scenes = segment_into_scenes(subs)[:2]  # Only first 2 scenes
for i, scene in enumerate(scenes, 1):
    print(f"\nScene {i}:\n", scene)
    print("\nAnalyzing with LLM...")
    result = analyze_scene(scene["transcript"])
    print("LLM Annotation Output:")
    print(result)
    print("-" * 40)