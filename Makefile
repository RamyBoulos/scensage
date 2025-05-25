.PHONY: test run hf-run mistral-run docker-build docker-mistral-run docker-hf-run help

SRT=tests/data/plan9.srt
LIMIT=20
OUT=scenes.json

# Run all unit tests with correct PYTHONPATH
test:
	PYTHONPATH=. pytest

# Run the SceneSage CLI tool with a default limit of 20 scenes
# The model used is determined by the USE_LOCAL environment variable
run:
	USE_LOCAL=$(USE_LOCAL) python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT)

# Run SceneSage using Hugging Face API (default if USE_LOCAL is not set)
hf-run:
	USE_LOCAL=none $(MAKE) run

# Run SceneSage locally using the Mistral model
mistral-run:
	USE_LOCAL=mistral $(MAKE) run

# Build the Docker image
docker-build:
	docker build -t scenesage .

# Run SceneSage in Docker using Mistral via Ollama
docker-mistral-run:
	docker run --rm -v $(shell pwd):/app -w /app -e USE_LOCAL=mistral scenesage python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT)

# Run SceneSage in Docker using Hugging Face API
docker-hf-run:
	docker run --rm -v $(shell pwd):/app -w /app -e USE_LOCAL=none scenesage python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT)

help:
	@echo "Usage:"
	@echo "  make test                  Run unit tests"
	@echo "  make run                   Run SceneSage locally (uses Ollama if USE_LOCAL=mistral, or Hugging Face API if USE_LOCAL=none)"
	@echo "  make hf-run                Run SceneSage locally with Hugging Face API"
	@echo "  make mistral-run           Run SceneSage locally with Mistral via Ollama"
	@echo "  make docker-build          Build the Docker image"
	@echo "  make docker-mistral-run    Run in Docker with Mistral via Ollama (local model, Ollama server required outside Docker)"
	@echo "  make docker-hf-run         Run in Docker with Hugging Face API (no Ollama needed)"
	@echo ""
	@echo "Notes:"
	@echo "  - For Docker Mistral runs, make sure Ollama is running on your host machine (not inside the container)."
	@echo "  - USE_LOCAL=mistral enables local inference via Ollama; USE_LOCAL=none (or unset) uses Hugging Face API."
