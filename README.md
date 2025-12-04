# product-parser

Small CLI tool to extract structured product data (title, brand, price, description, attributes) from e-commerce HTML files using a staged parsing pipeline.

## Quickstart

1. Create and activate a venv (bash):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install -e .
   ```

2. Run the CLI:

   - Use the default input file defined in `src/product_parser/config.py`:

     ```bash
     parse-product
     # or
     python -m product_parser.cli
     ```

   - Provide a custom file with `--input` / `-i`:

     ```bash
     parse-product --input test_data/input.html
     python -m product_parser.cli --input test_data/input.html
     ```

## Build

```bash
python -m pip install --upgrade build
python -m build
python -m pip install dist/*
```

## Testing

Install pytest and add tests under `tests/`, then run:

```bash
python -m pip install pytest
pytest -q
```

## Notes

- Default input path: `HTML_INPUT_FILE` in `src/product_parser/config.py` (currently `test_data/input2.html`).
- If you use LLMs, set `OPENAI_API_KEY` in the environment or a `.env` file.

## Project layout (brief)

- `src/product_parser/cli.py` — entry point (now supports `--input`)
- `src/product_parser/parser.py` — pipeline orchestration
- `src/product_parser/models.py` — Pydantic models
- `src/product_parser/llm_pipeline.py` — LLM chains
- `test_data/` — example inputs

## License

Add a `LICENSE` file (e.g., MIT) if you want to make reuse terms explicit.

## Contributing

Fork, add tests, and open a PR.
