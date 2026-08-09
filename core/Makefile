.DEFAULT_GOAL := default

.PHONY: test
test:
	uv run --no-sync pytest --cov=Final2x_core --cov-report=xml --cov-report=html

.PHONY: lint
lint:
	uv run --no-sync ruff check .
	uv run --no-sync ruff format --check .
	uv run --no-sync mypy Final2x_core tests

.PHONY: gen
gen:
	uv run --no-sync python scripts/gen_config.py

.PHONY: gen-ts
gen-ts:
	uv run --no-sync python scripts/gen_pretrained_model_name.py --output ../../src/renderer/src/utils/modelOptions.ts

.PHONY: build
build:
	uv build

.PHONY: pyinstaller
pyinstaller:
	uv run --no-sync pyinstaller -n Final2x-core -i assets/favicon.ico Final2x_core/__main__.py
	uv run --no-sync python scripts/post_pyinstaller.py
