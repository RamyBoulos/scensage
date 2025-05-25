###############################################################################
#                          SceneSage Project - Makefile                      #
###############################################################################

# ===[ CONFIGURATION VARIABLES ]==============================================
SRT        := tests/data/plan9.srt
LIMIT      := 20
OUT        := scenes.json
MODEL      := mistralai/Mixtral-8x7B-Instruct-v0.1

# ===[ TESTING & QUALITY ]====================================================
.PHONY: test
test:
	PYTHONPATH=. pytest

# ===[ LOCAL EXECUTION ]======================================================
.PHONY: run
run:
	USE_LOCAL=$${USE_LOCAL:-none} python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT) --model $(MODEL)

# ===[ SHORTCUTS: LOCAL/HF RUNS ]=============================================
.PHONY: hf-run mistral-gap mistral-llm mistral-run
hf-run:   # Run with Hugging Face API (default; USE_LOCAL=none)
	USE_LOCAL=none $(MAKE) run

mistral-run:   # Run with local Mistral via Ollama (USE_LOCAL=mistral)
	USE_LOCAL=mistral $(MAKE) run

# ===[ ADVANCED: SEGMENTATION STRATEGIES ]====================================
.PHONY: run-llm run-gap
run-llm:   # LLM segmentation, HF inference
	USE_LOCAL=none python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT) --strategy llm --model $(MODEL)

run-gap:   # GAP segmentation, HF inference
	USE_LOCAL=none python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT) --strategy gap --model $(MODEL)

.PHONY: mistral-gap mistral-llm
mistral-llm:   # LLM segmentation, local Mistral
	USE_LOCAL=mistral python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT) --strategy llm --model $(MODEL)

mistral-gap:   # GAP segmentation, local Mistral
	USE_LOCAL=mistral python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT) --strategy gap --model $(MODEL)

# ===[ DOCKER WORKFLOWS ]=====================================================
.PHONY: docker-build docker-mistral-run docker-hf-run
docker-build:    # Build Docker image
	docker build -t scenesage .

docker-mistral-run:    # Run in Docker with local Mistral (Ollama must be running outside Docker)
	docker run --rm -v $(shell pwd):/app -w /app -e USE_LOCAL=mistral scenesage python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT) --model $(MODEL)

docker-hf-run:    # Run in Docker with Hugging Face API
	docker run --rm -v $(shell pwd):/app -w /app -e USE_LOCAL=none scenesage python3 -m scenesage.scenesage $(SRT) --limit $(LIMIT) --output $(OUT) --model $(MODEL)

# ===[ HELP ]==================================================================
.PHONY: help
help:
	@echo "=========================="
	@echo "   SceneSage Makefile Help"
	@echo "=========================="
	@echo ""
	@echo "  make test                 Run unit tests"
	@echo "  make run                  Run SceneSage with selected model (set USE_LOCAL and MODEL as needed)"
	@echo "  make hf-run               Run SceneSage with Hugging Face API (default)"
	@echo "  make mistral-run          Run SceneSage locally with Mistral via Ollama"
	@echo ""
	@echo "  make run-llm              Run SceneSage with LLM segmentation (HF API)"
	@echo "  make run-gap              Run SceneSage with GAP segmentation (HF API)"
	@echo "  make mistral-llm          Run with LLM segmentation and local Mistral"
	@echo "  make mistral-gap          Run with GAP segmentation and local Mistral"
	@echo ""
	@echo "  make docker-build         Build Docker image"
	@echo "  make docker-mistral-run   Run in Docker with Mistral/Ollama (host Ollama required)"
	@echo "  make docker-hf-run        Run in Docker with Hugging Face API"
	@echo ""
	@echo "Variables:"
	@echo "  SRT     Path to SRT file [$(SRT)]"
	@echo "  LIMIT   Number of scenes to process [$(LIMIT)]"
	@echo "  OUT     Output file [$(OUT)]"
	@echo "  MODEL   Model for annotation [$(MODEL)]"
	@echo ""
	@echo "Set USE_LOCAL=mistral to use local Ollama, or USE_LOCAL=none (default) for Hugging Face API."
	@echo ""
	@echo "Examples:"
	@echo "  make run MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1"
	@echo "  make run-llm LIMIT=5 OUT=result.json"
	@echo ""
	@echo "Enjoy SceneSage!"
