import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool

from tools.llm_provider import get_llm  # Import the shared LLM provider
from tools.tools import get_profile_url_tavily

LINKEDIN_PROMPT_TEMPLATE = """
You are a helpful assistant that knows how to look up information about people on LinkedIn.
Given the name {query}, please provide the exact LinkedIn profile page URL.
Your answer must be a single, valid URL (starting with http:// or https://) and nothing else.
"""

load_dotenv()

def build_agent_executor(llm, tools):
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


def lookup(query: str) -> str:
    load_dotenv()  # Ensure environment variables are loaded
    llm = get_llm(temperature=0, provider=os.getenv("MODEL_PROVIDER"))

    prompt_template = PromptTemplate.from_template(LINKEDIN_PROMPT_TEMPLATE)
    tools_for_agent = [
        Tool(
            name="Crawl Google for Linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the LinkedIn Page URL",
        )
    ]

    agent_executor = build_agent_executor(llm, tools_for_agent)
    formatted_prompt = prompt_template.format_prompt(query=query)
    lookup_result = agent_executor.invoke(input={"input": formatted_prompt})
    linkedin_profile_url = lookup_result["output"]

    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(query="Udemy's Eden Marco Linkedin Profile")
    print(linkedin_url)
