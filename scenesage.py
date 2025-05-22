import argparse
import json
from parser import parse_srt_file, segment_into_scenes
from annotator import analyze_scene

def main():
    parser = argparse.ArgumentParser(description="SceneSage - LLM-powered Scene Analyzer")
    parser.add_argument("srt_file", help="Path to the .srt subtitle file or URL")
    parser.add_argument("--model", default="mistralai/Mixtral-8x7B-Instruct-v0.1", help="Hugging Face model name")
    parser.add_argument("--output", default="scenes.json", help="Path to the output JSON file")
    parser.add_argument("--limit", type=int, help="Limit the number of scenes to process (optional)")

    args = parser.parse_args()

    print(f"Parsing subtitle file: {args.srt_file}")
    subs = parse_srt_file(args.srt_file)

    print("Segmenting into scenes...")
    scenes = segment_into_scenes(subs)
    if args.limit:
        scenes = scenes[:args.limit]

    print(f"Annotating {len(scenes)} scenes using {args.model}...")
    annotated_scenes = []
    for i, scene in enumerate(scenes, 1):
        print(f"Analyzing scene {i}/{len(scenes)}")
        annotations = analyze_scene(scene["transcript"], model=args.model)
        annotated_scene = {
            "start": scene["start"],
            "end": scene["end"],
            "transcript": scene["transcript"],
            **annotations
        }
        annotated_scenes.append(annotated_scene)

    print(f"Writing output to {args.output}")
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(annotated_scenes, f, indent=2, ensure_ascii=False)

    print("Done.")

if __name__ == "__main__":
    main()