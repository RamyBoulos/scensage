

# SceneSage

**SceneSage** is a Python-based command-line tool for enriching video subtitles with AI-generated scene annotations. It processes `.srt` subtitle files, segments them into scenes, and uses Large Language Models (LLMs) to annotate each scene with a summary, characters, mood, and cultural references.

Supports both remote inference via Hugging Face API (default) and local inference using the Mistral 7B model via Ollama.

Repository: [github.com/RamyBoulos/scensage](https://github.com/RamyBoulos/scensage)

---

## Features

- 🎬 **Scene Segmentation** – Groups subtitles into coherent scenes using LLM or time-gap strategy.
- 🤖 **LLM Annotation** – Adds summaries, character info, mood, and cultural references to each scene.
- 🔌 **Hugging Face & Ollama** – Use Hugging Face models (default) or local Mistral via Ollama.
- 🐳 **Docker Support** – Run SceneSage in a containerized environment.
- 🛠️ **Makefile Shortcuts** – Convenient commands for testing and running locally or in Docker.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RamyBoulos/scensage.git
cd scensage
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: This does not install a CLI command globally. Run via `python3 -m scenesage.scenesage` or use the Makefile/Docker.

---

## Usage

### 🔧 Set Up Environment Variables

- For Hugging Face API:

```bash
export HUGGINGFACEHUB_API_TOKEN=your_hf_token
export USE_LOCAL=none
```

- For local Ollama inference:

```bash
export USE_LOCAL=mistral
ollama run mistral  # Make sure Mistral is pulled and running
```

---

### ▶️ Command-Line Example

```bash
python3 -m scenesage.scenesage path/to/input.srt --output scenes.json --model mistralai/Mixtral-8x7B-Instruct-v0.1
```

---

### 🛠️ Makefile Shortcuts

The Makefile includes convenient commands for different use cases.

#### Run with Hugging Face API (default)

```bash
make hf-run
```

#### Run with local Mistral via Ollama

```bash
make mistral-run
```

#### Segmentation strategies

```bash
make run-llm         # LLM-based segmentation with HF
make run-gap         # Time-gap segmentation with HF
make mistral-llm     # LLM segmentation + local Mistral
make mistral-gap     # GAP segmentation + local Mistral
```

---

### 🐳 Docker Usage

#### Build Docker Image

```bash
make docker-build
```

#### Run with Hugging Face

```bash
make docker-hf-run
```

#### Run with local Mistral (Ollama must be running on host)

```bash
make docker-mistral-run
```

> The Docker container communicates with the Ollama host at `host.docker.internal`. You must have Mistral running via Ollama **outside Docker**.

---

## File Structure

```
scenesage/
├── scenesage/             # Core source code
│   ├── scenesage.py       # CLI entry point
│   ├── annotator.py       # LLM scene annotation
│   ├── parser.py          # SRT parsing and scene segmentation
│   ├── utils.py           # Timestamp parsing, JSON extraction
│   └── ...
├── tests/                 # Unit tests
├── Dockerfile             # Docker config
├── Makefile               # Run shortcuts
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

**Ramy Boulos**  
[github.com/RamyBoulos](https://github.com/RamyBoulos)