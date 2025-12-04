import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY is not set. Please export it or put it in .env")

HTML_INPUT_FILE = "test_data/input2.html"

STAGE_0_HTML_CLEANUP = True
STAGE_0_HTML_TO_MD = True

SAVE_INTERMEDIATE_HTML = True
SAVE_INTERMEDIATE_MD = True

# Global configs and paths (default)
OUTPUT_FOLDER = "saved-pages"

### ----------------------------------------------------------

STAGE_1_PROMPT = """
You analyze cleaned HTML content of an e-commerce page.

Tasks:
1) Decide if this is a product page (true/false).
2) Identify content language
3) If it is, briefly extract the following blocks:
   - product title
   - product availability
   - product price text (as seen on the page)
   - about the product or product description block (make a summary)
   - technical details block (if any)

Return the result strictly as a JSON object matching the given schema.

HTML:
{stage_0_result}
"""

STAGE_2_PROMPT = """
You are a highly accurate product-page parser.

Your task is to build a normalized Product object based on the Stage-1 analysis.

Use this schema:
- title: main product name
- brand: product brand if available
- price_value: numeric price (float) if you can extract it
- price_currency: 3-letter currency codes
- old_price_value: previous/original price if there is a discount
- description: main textual description
- attributes: key-value map of product attributes (components, size, color, material, dimensions, etc.)

If some fields are unknown, set them to null or keep lists/maps empty.

Stage-1 analysis (JSON format):
{product_info}
"""

