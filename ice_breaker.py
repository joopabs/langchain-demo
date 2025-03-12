import logging
from dotenv import load_dotenv
from rich import print
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile

from tools.llm_provider import get_llm  # Use the shared LLM provider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUMMARY_PROMPT_TEMPLATE = """
You are a helpful assistant that knows how to extract useful data from JSON --
Given the following data from a LinkedIn profile:
{information}

Please create the following:
1. A short summary of the person.
2. Two interesting facts about them.

Kindly provide the answers directly, without any additional context.
"""


def get_prompt_template():
    return PromptTemplate.from_template(SUMMARY_PROMPT_TEMPLATE)


def build_pipeline(llm, with_output_parser: bool = True):
    prompt_template = get_prompt_template()
    if with_output_parser:
        output_parser = StrOutputParser()
        return prompt_template | llm | output_parser
    return prompt_template | llm


def stream_information_processing(information: str):
    llm = get_llm(temperature=0)
    pipeline = build_pipeline(llm, with_output_parser=False)
    for chunk in pipeline.stream(input={"information": information}):
        if hasattr(chunk, "content"):
            print(chunk.content, end="", flush=True)


def main():
    linkedin_url = "https://www.linkedin.com/in/julius-p-0052794/"
    information = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)
    stream_information_processing(information)


if __name__ == "__main__":
    load_dotenv()
    main()
    print()
