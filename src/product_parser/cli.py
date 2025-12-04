from pathlib import Path
import argparse
from typing import Optional, List

from .parser import extract_product_data
from .config import HTML_INPUT_FILE
from .logging_config import logger


def resolve_input_path(argv: Optional[List[str]] = None) -> str:
    """Return the resolved input path.

    Priority:
    1. `--input`/`-i` CLI argument from `argv` if provided
    2. `HTML_INPUT_FILE` from config as fallback
    """
    parser = argparse.ArgumentParser(
        prog="parse-product",
        description="Extract product information from an HTML file",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Path to input HTML file (defaults to value of HTML_INPUT_FILE in config)",
        default=None,
    )
    args = parser.parse_args(argv)
    return args.input or HTML_INPUT_FILE


def main(argv: Optional[List[str]] = None):
    """Run the CLI. Resolve the HTML input path (via argparse), read file, run extraction and print JSON result."""
    resolved_input = resolve_input_path(argv)

    html_path = Path(resolved_input)

    if not html_path.exists():
        logger.error(f"HTML input file not found: {html_path}")
        raise SystemExit(1)

    logger.info(f"Reading HTML file: {html_path}")

    raw_html = html_path.read_text(encoding="utf-8", errors="ignore")

    product = extract_product_data(raw_html)
    if product is None:
        logger.error("Product extraction returned no result")
        raise SystemExit(2)

    print("Parsing result:")
    print(product.model_dump_json())


if __name__ == "__main__":
    main()