# product-parser

Extract structured product information from e-commerce HTML pages using a small, staged parsing pipeline.

A lightweight command-line tool and library that reads an HTML file, runs an extraction pipeline (cleanup, light analysis, and structured parsing), and prints a normalized Product JSON object.

Features

- Staged parsing pipeline: HTML cleanup -> lightweight analysis -> structured product extraction
- Pydantic models for typed output
- CLI entry point for quick runs
- Designed to be extended with LLM-based parsing in `llm_pipeline.py`

Requirements

- Python 3.9+
- Recommended: use a virtual environment
- Dependencies are listed in `pyproject.toml` (notably: requests, beautifulsoup4, lxml, markdownify, langchain-core, langchain-openai, pydantic, python-dotenv)

Quickstart — development

1. Create and activate a virtual environment (bash):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the package in editable mode:

   ```bash
   python -m pip install -e .
   ```

3. Run the CLI

   - Using the installed script (entry point defined in `pyproject.toml`):

     ```bash
     parse-product
     ```

   - Or run the module directly (uses `HTML_INPUT_FILE` from `src/product_parser/config.py`):

     ```bash
     python -m product_parser.cli
     ```

By default the CLI reads the file defined in `HTML_INPUT_FILE` inside `src/product_parser/config.py` (currently: `test_data/input2.html`). To run with a different file you can either edit that constant in `config.py` or run a tiny wrapper script. Example wrapper to run a different input without editing the package:

```bash
python - <<'PY'
from product_parser import config
from product_parser.cli import main
config.HTML_INPUT_FILE = 'test_data/input.html'
main()
PY
```

Build / distribution

Create source and wheel distributions (requires the `build` package):

```bash
python -m pip install --upgrade build
python -m build
```

Install a built artifact locally:

```bash
python -m pip install dist/*
```

Testing

This repository does not include tests by default. To add and run tests:

1. Install pytest:

   ```bash
   python -m pip install pytest
   ```

2. Create tests in a `tests/` directory (for example `tests/test_parser.py`) and run:

   ```bash
   pytest -q
   ```

Running with example data

The repository includes `test_data/input.html` and `test_data/input2.html`. To test the CLI against those files, either update `HTML_INPUT_FILE` or use the wrapper script shown above.

Configuration & environment

- `src/product_parser/config.py` contains runtime defaults. Important values:
  - `HTML_INPUT_FILE` — default path to the input HTML used by the CLI (default: `test_data/input2.html`).
  - `OPENAI_API_KEY` — the code reads this env var (via `python-dotenv`) and will warn if it is not set. If the project is extended to call OpenAI, set this environment variable before running (for example `export OPENAI_API_KEY=sk-...`).

Project layout (important files)

- `pyproject.toml` — project metadata and dependencies
- `src/product_parser/cli.py` — CLI entry point (reads HTML file and prints result)
- `src/product_parser/parser.py` — staged pipeline orchestration (stage0/1/2)
- `src/product_parser/models.py` — Pydantic models for stage analysis and final Product
- `src/product_parser/llm_pipeline.py` — (adapter) chains for stage processing (LLM hooks)
- `src/product_parser/html_cleaner.py` — HTML cleanup helpers
- `src/product_parser/config.py` — runtime configuration and prompts
- `test_data/` — example input HTML files

Troubleshooting

- If you see a warning about `OPENAI_API_KEY` being missing, set it in your environment or a `.env` file in the project root.
- If the CLI fails because `HTML_INPUT_FILE` cannot be found, update the path in `src/product_parser/config.py` or pass a custom input using the wrapper approach shown above.
- If you extend LLM functionality, ensure network access and valid API keys for the provider you use.

License

This repository does not declare a license file. Add a `LICENSE` (for example MIT) to indicate how the project may be used.

Proactive extras (suggested next steps)

- Add a `tests/` directory with at least one smoke test for `extract_product_data` using `test_data/` files.
- Add a `--input` CLI argument to `product_parser.cli:main` so the input path does not need to be edited in `config.py`.
- Add CI (GitHub Actions) to run linting and tests on push.

Contributing

Contributions are welcome. Fork the repository, add tests for new behavior, and open a pull request.
