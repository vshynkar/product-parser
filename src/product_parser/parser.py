from typing import Optional

from .config import STAGE_0_HTML_CLEANUP, STAGE_0_HTML_TO_MD
from .html_cleaner import html_cleanup, html_to_markdown
from .io_utils import format_size
from .llm_pipeline import stage1_chain, stage2_chain
from .logging_config import logger
from .models import Stage1Analysis, Product


def stage0_processing(raw_html: str) -> str:
    processed_text = raw_html

    if STAGE_0_HTML_CLEANUP:
        logger.info(f"Input HTML data cleanup")
        processed_text = html_cleanup(raw_html)

    if STAGE_0_HTML_TO_MD:
        logger.info(f"Convert HTML to Markdown")
        processed_text = html_to_markdown(processed_text)
    return processed_text


def stage1_processing(input_data: str) -> Optional[Stage1Analysis]:
    # Stage-1: classification + light extraction
    analysis: Stage1Analysis = stage1_chain.invoke({"stage_0_result": input_data})

    if analysis is None:
        logger.error("Stage-1 processing failed")
        return None

    if not analysis.is_product_page:
        logger.warn("Input page is not a product page")
        return None

    return analysis


def stage2_processing(input_data: str) -> Optional[Product]:
    analysis: Product = stage2_chain.invoke({"product_info": input_data})

    if analysis is None:
        logger.error("Stage-2 processing failed")
        return None

    return analysis


def extract_product_data(raw_html: str) -> Optional[Product]:
    logger.info(f"Start product extraction process. Input file size is {format_size(len(raw_html))}")

    logger.info(f"Start Stage 0 input data cleanup process.")
    stage0_result = stage0_processing(raw_html)
    logger.info(f"Stage 0 input data cleanup process finished. Result size is {format_size(len(stage0_result))}")

    logger.info(f"Start Stage 1 product data parsing.")
    stage1_result = stage1_processing(stage0_result)
    logger.info(f"Stage 1 processing finished")

    if stage1_result is None:
        logger.warn(f"Product extraction process failed due to some reason. Stop extraction process.")
        return None

    logger.info(f"Start Stage 2 product data parsing.")
    stage2_result = stage2_processing(stage1_result.model_dump_json())
    logger.info(f"Stage 2 processing finished")

    logger.info(f"Product extraction process finished")

    return stage2_result