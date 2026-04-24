.PHONY: setup lint format typecheck test test-unit test-integration openapi run

# Install all dependencies (runtime + dev) and activate pre-commit hooks.
# Run this once after cloning the repository.
setup:
	pipenv install --dev
	pipenv run pre-commit install

# Run the linter (ruff). Does not modify files.
lint:
	pipenv run ruff check src/main/event_resolver/ src/test/

# Auto-format all source files (ruff + black).
format:
	pipenv run ruff format src/main/event_resolver/ src/test/
	pipenv run black src/main/event_resolver/ src/test/

# Run static type checking (excludes auto-generated code).
typecheck:
	pipenv run mypy src/main/event_resolver/ --ignore-missing-imports

# Run all tests (unit + integration).
test:
	pipenv run pytest src/test/python/ -v

# Run unit tests only (fast, no network).
test-unit:
	pipenv run pytest src/test/python/unit/ -v

# Run integration tests only.
test-integration:
	pipenv run pytest src/test/python/test_events/ -v

# Regenerate server models from the remote OpenAPI spec.
openapi:
	bash scripts/openapi.sh

# Run the development server.
run:
	PYTHONPATH=src/main:src/main/@generated pipenv run python -m main
