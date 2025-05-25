# SceneSage 🎬

**SceneSage** is a powerful command-line interface (CLI) tool designed to automate scene analysis from `.srt` subtitle files using large language models (LLMs). It parses subtitle files, segments scenes based on customizable strategies, and generates detailed, structured annotations for each scene—such as summaries, character mentions, emotional tone, and cultural references—via the Hugging Face Inference API.

---

## Table of Contents

- [Features](#features)  
- [Scene Segmentation Strategies](#scene-segmentation-strategies)  
- [Inference Modes](#inference-modes)  
- [Installation](#installation)  
- [Setup](#setup)  
- [Usage](#usage)  
- [Makefile Shortcuts](#makefile-shortcuts)  
- [Output Examples](#output-examples)  
- [License](#license)  
- [Acknowledgments](#acknowledgments)  

---

## Features

- Parses `.srt` subtitle files with robust handling of common formats  
- Supports multiple scene segmentation strategies: time gaps, fixed cue counts, and scene change detection  
- Integrates with Hugging Face Inference API for LLM-powered scene annotation  
- Outputs structured JSON annotations including:  
  - Scene start and end timestamps  
  - Concatenated transcript text  
  - One-sentence summary  
  - Character mentions  
  - Mood/emotion analysis  
  - Up to three cultural references  
- CLI interface with options for model selection, scene limits, segmentation method, and output file specification  
- Designed for extensibility and ease of integration into media analysis pipelines  

---

## Scene Segmentation Strategies

SceneSage supports flexible scene segmentation to adapt to different types of subtitle files and user needs:

- **Time Gap Segmentation (`timegap`)**  
  Scenes are segmented when there is a gap equal to or greater than a specified threshold (default: 4 seconds) between subtitle cues.

- **Fixed Cue Count Segmentation (`fixedcount`)**  
  Scenes are segmented by grouping a fixed number of subtitle cues (e.g., every 10 cues).

- **Scene Change Detection (`scenechange`)**  
  (Experimental) Attempts to detect scene changes based on subtitle content or metadata.

You can select the segmentation method with the `--segment` flag and customize parameters such as the time gap threshold or cue count.

---

## Inference Modes

SceneSage supports different inference modes to balance speed and quality:

- **Streaming Mode**  
  Processes scenes sequentially and streams partial results for faster feedback.

- **Batch Mode**  
  Processes all scenes in a single batch request for efficiency.

Currently, streaming mode is the default and recommended for most use cases.

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/RamyBoulos/scenesage.git
cd scenesage

# (Optional) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

---

## Setup

### Hugging Face API Token

SceneSage requires a Hugging Face Inference API token to access language models:

1. Create a `.env` file in the project root directory with the following content:

   ```
   HUGGINGFACEHUB_API_TOKEN=your_token_here
   ```

2. Obtain your token from [Hugging Face Tokens Page](https://huggingface.co/settings/tokens).

3. Ensure you have access to a text-generation capable model, such as `mistralai/Mixtral-8x7B-Instruct-v0.1`.

---

## Usage

### Basic Command

```bash
python scenesage.py your_subtitle_file.srt --output scenes.json
```

### Common Options

| Option           | Description                                               | Default                            |
|------------------|-----------------------------------------------------------|----------------------------------|
| `--model`        | Hugging Face model to use                                  | `mistralai/Mixtral-8x7B-Instruct-v0.1` |
| `--limit`        | Process only the first N scenes (for testing)             | Process all                      |
| `--segment`      | Scene segmentation method: `timegap`, `fixedcount`, `scenechange` | `timegap`                      |
| `--gap`          | Time gap threshold in seconds for `timegap` segmentation  | `4` seconds                     |
| `--count`        | Number of cues per scene for `fixedcount` segmentation    | `10` cues                      |
| `--output`       | Output JSON file path                                      | `scenes.json`                   |

### Example

Process the first 10 scenes from `plan9.srt` using the default model and time gap segmentation:

```bash
python scenesage.py plan9.srt --limit 10 --output scenes.json
```

Use fixed cue count segmentation with 15 cues per scene:

```bash
python scenesage.py plan9.srt --segment fixedcount --count 15 --output scenes.json
```

Specify a different model:

```bash
python scenesage.py plan9.srt --model google/flan-t5-large --output scenes.json
```

---

## Makefile Shortcuts

If you prefer using `make`, the following shortcuts are available:

- **Run analysis on sample clip:**

  ```bash
  make run
  ```

- **Run analysis with first 10 scenes:**

  ```bash
  make run-limit
  ```

- **Clean output files:**

  ```bash
  make clean
  ```

---

## Output Examples

Below are sample outputs generated by SceneSage for a subtitle excerpt.

### Input Subtitle Excerpt (`clip.srt`):

```
1
00:00:22,719 --> 00:00:26,759
Greetings, my friend. We are all interested in the future,

2
00:00:26,860 --> 00:00:31,507
for that is where you and I are going to spend the rest of our lives.
```

### Corresponding JSON Output (`scenes.json`):

```json
[
  {
    "start": "00:00:22,719",
    "end": "00:00:31,507",
    "transcript": "Greetings, my friend. We are all interested in the future, for that is where you and I are going to spend the rest of our lives.",
    "summary": "The narrator reflects on humanity's fascination with the future.",
    "characters": ["Narrator"],
    "mood": "thoughtful",
    "cultural_refs": []
  }
]
```

*Note:* Your actual output may vary depending on the model and parameters used.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- Subtitle data courtesy of [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Plan_9_from_Outer_Space_(1959).webm)  
- Language model inference via [Hugging Face Inference API](https://huggingface.co/inference-api)  
- Inspired by the need for automated media analysis and annotation tools  

---

Thank you for using SceneSage! If you have any questions or feedback, please open an issue or submit a pull request on GitHub.