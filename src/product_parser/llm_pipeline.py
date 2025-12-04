from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .logging_config import logger

from .config import STAGE_1_PROMPT, STAGE_2_PROMPT
from .models import Stage1Analysis, Product


# --------- Token usage logger ---------

class TokenUsageLogger(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        try:
            usage = response.llm_output.get("token_usage", {})
            prompt_toks = usage.get("prompt_tokens")
            completion_toks = usage.get("completion_tokens")
            total_toks = usage.get("total_tokens")
            logger.info(
                f"Token usage → prompt={prompt_toks}, "
                f"completion={completion_toks}, total={total_toks}"
            )
        except Exception as e:
            logger.error(f"Failed to extract token usage: {e}")

token_usage_logger = TokenUsageLogger()

# --------- OpenAI models ---------
nano_llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0,
    max_retries=2,
    callbacks=[token_usage_logger]
)

deep_llm = ChatOpenAI(
    model="gpt-5.1",
    temperature=0,
    max_retries=2,
    callbacks=[token_usage_logger]
)

stage1_prompt = ChatPromptTemplate.from_template(STAGE_1_PROMPT)
nano_structured = nano_llm.with_structured_output(Stage1Analysis)
stage1_chain = stage1_prompt | nano_structured

stage2_prompt = ChatPromptTemplate.from_template(STAGE_2_PROMPT)
deep_structured = deep_llm.with_structured_output(Product)
stage2_chain = stage2_prompt | deep_structured

