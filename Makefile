install:
	uv sync

sync:
	uv sync

run:
	uv run python3 -m src

visual:
	uv run python3 -m src --visualize

debug:
	uv run python3 -m pdb -m src

clean:
	rm -rf .mypy_cache

lint:
	uv run python3 -m flake8 src
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run python3 -m flake8 src
	mypy . --strict