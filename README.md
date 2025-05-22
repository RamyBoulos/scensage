# SceneSage 🎬  
LLM-powered CLI tool for automated scene analysis from `.srt` subtitle files.

SceneSage parses subtitle files, detects scene breaks, and uses a Hugging Face language model to generate rich, structured annotations for each scene — including summaries, character mentions, emotional tone, and cultural references.

---

## ✨ Features

- 🔍 Parses `.srt` subtitle files
- ⏱️ Segments scenes based on time gaps ≥ 4 seconds
- 🤖 Sends each scene to an LLM via Hugging Face API
- 📄 Returns structured JSON annotations:
  - One-sentence summary
  - Character mentions
  - Mood/emotion
  - Up to 3 cultural references
- ✅ CLI interface with model selection and output file support

---

## 📦 Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/RamyBoulos/scensage.git
cd scensage

# (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Setup: Hugging Face API Key

SceneSage requires access to the Hugging Face Inference API.

1. Create a `.env` file in the project root:
```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

2. Get your token from: https://huggingface.co/settings/tokens  
(You’ll need a model that supports text generation like `mistralai/Mixtral-8x7B-Instruct-v0.1`.)

---

## 🚀 Usage

### Basic CLI

```bash
python scenesage.py your_subtitle_file.srt --output scenes.json
```

### Optional flags

- `--model` : Use a specific Hugging Face model (default: `mistralai/Mixtral-8x7B-Instruct-v0.1`)
- `--limit` : Process only the first N scenes (useful for testing)

### Example

```bash
python scenesage.py plan9.srt --model mistralai/Mixtral-8x7B-Instruct-v0.1 --limit 10 --output scenes.json
```

---

## 🧪 Sample Input/Output

### 🎞️ Sample input (`.srt` excerpt):
```
1
00:00:22,719 --> 00:00:26,759
Greetings, my friend. We are all interested in the future,

2
00:00:26,860 --> 00:00:31,507
for that is where you and I are going to spend the rest of our lives.
```

### 📤 Sample output (`scenes.json`):
```json