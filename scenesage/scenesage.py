import argparse
import json
from .parser import parse_srt_file, segment_into_scenes
from .annotator import analyze_scene
from tqdm import tqdm

# By default, --model mistral uses local Ollama. Specify full Hugging Face model name for API use.

def main():
    parser = argparse.ArgumentParser(description="SceneSage - LLM-powered Scene Analyzer")
    parser.add_argument("srt_file", help="Path to the .srt subtitle file or URL")
    parser.add_argument(
        "--model",
        default="mistral",
        help="LLM model to use: 'mistral' for local Ollama Mistral, or Hugging Face model name (e.g., 'mistralai/Mistral-7B-Instruct-v0.1')"
    )
    parser.add_argument("--output", default="scenes.json", help="Path to the output JSON file")
    parser.add_argument("--limit", type=int, help="Limit the number of scenes to process (optional)")
    parser.add_argument(
        "--strategy",
        default="llm",
        choices=["llm", "gap"],
        help="Scene segmentation strategy: 'llm' for LLM-based or 'gap' for time-based"
    )
    parser.add_argument("--lang", default="English", help="Language for annotation output (default: English)")

    args = parser.parse_args()

    print(f"Parsing subtitle file: {args.srt_file}")
    subs = parse_srt_file(args.srt_file)

    segmentation_mode = args.strategy
    print(f"[INFO] Scene segmentation mode: {segmentation_mode}")

    print("Segmenting into scenes...")
    scenes = segment_into_scenes(subs, mode=segmentation_mode)
    if args.limit:
        scenes = scenes[:args.limit]

    print(f"Annotating {len(scenes)} scenes using {args.model}...")
    annotated_scenes = []
    for i, scene in enumerate(tqdm(scenes, desc="Analyzing scenes"), 1):
        print(f"Analyzing scene {i}/{len(scenes)}")
        annotations = analyze_scene(scene["transcript"], model=args.model, language=args.lang)
        annotated_scene = {
            "start": scene["start"],
            "end": scene["end"],
            "transcript": scene["transcript"],
            "segmentation_mode": segmentation_mode,
            **annotations
        }
        annotated_scenes.append(annotated_scene)

    print(f"Writing output to {args.output}")
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(annotated_scenes, f, indent=2, ensure_ascii=False)

    print("Done.")

if __name__ == "__main__":
    main()