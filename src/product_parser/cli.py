from pathlib import Path

from product_parser.models import Product
from .parser import extract_product_data
from .config import HTML_INPUT_FILE
from .logging_config import logger


def main():
    html_path = Path(HTML_INPUT_FILE)

    if not html_path.exists():
        logger.error(f"HTML input file not found: {html_path}")
        raise SystemExit(1)

    logger.info(f"Reading HTML file: {html_path}")

    raw_html = html_path.read_text(encoding="utf-8", errors="ignore")

    product: Product = extract_product_data(raw_html)
    print('Parsing result:')
    print(product.model_dump_json())


if __name__ == "__main__":
    main()