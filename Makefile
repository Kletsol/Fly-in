install:
	uv sync

sync:
	uv sync

ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

.PHONY: run $(ARGS)

run:
	uv run python3 -m src $(ARGS)

$(ARGS):
	@:

debug:
	uv run python3 -m pdb -m src

clean:
	rm -rf .mypy_cache

lint:
	uv run python3 -m flake8 src
	uv run python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run python3 -m flake8 src
	uv run python3 -m mypy . --strict