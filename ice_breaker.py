import logging
from dotenv import load_dotenv
from rich import print
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LLM_PROVIDER = "ollama"  # Change this to different value switch providers


def get_llm(temperature: int = 0):
    """
    Returns an instance of the desired LLM based on the LLM_PROVIDER constant.
    """
    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI

        logger.info("Using ChatOpenAI as LLM provider")
        return ChatOpenAI(temperature=temperature, model="gpt-3.5-turbo")
    else:
        from langchain_ollama import ChatOllama

        logger.info("Using ChatOllama as LLM provider")
        return ChatOllama(temperature=temperature, model="llama3")


# Constant for the summary prompt template
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
    """Creates and returns a prompt template based on the summary prompt."""
    return PromptTemplate.from_template(SUMMARY_PROMPT_TEMPLATE)


def build_pipeline(llm, with_output_parser: bool = True):
    """
    Builds and returns a LangChain pipeline.
    If with_output_parser is True, the pipeline will include the output parser.
    """
    prompt_template = get_prompt_template()
    if with_output_parser:
        output_parser = StrOutputParser()
        return prompt_template | llm | output_parser
    return prompt_template | llm


def stream_information_processing(information: str):
    """Processes the information using the LangChain pipeline and streams the result."""
    llm = get_llm(temperature=0)
    pipeline = build_pipeline(llm, with_output_parser=False)
    for chunk in pipeline.stream(input={"information": information}):
        if hasattr(chunk, "content"):
            print(chunk.content, end="", flush=True)


def main():
    """Main function to scrape a LinkedIn profile and process the extracted information."""
    linkedin_url = "https://www.linkedin.com/in/julius-p-0052794/"
    information = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)
    stream_information_processing(information)


if __name__ == "__main__":
    load_dotenv()
    main()
    print()
