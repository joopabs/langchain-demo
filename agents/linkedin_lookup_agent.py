from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from tools.tools import get_profile_url_tavily
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# Constants for prompt template and tool description
LINKEDIN_PROMPT_TEMPLATE = """
You are a helpful assistant that knows how to look up information about people on LinkedIn.
Given the name {query}, please provide the exact LinkedIn profile page URL.
Your answer must be a single, valid URL (starting with http:// or https://) and nothing else.
"""


def get_llm(llm_name: str):
    """
    Return an instance of the chosen language model.
    Supported values: 'ollama', 'chatopenai', 'gemini'
    """
    llm_name = llm_name.lower()
    if llm_name == "ollama":
        return ChatOllama(temperature=0, model="mistral")
    elif llm_name == "openai":
        return ChatOpenAI(temperature=0, model="gpt-4o-mini")
    elif llm_name == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    else:
        raise ValueError(f"Unsupported LLM choice: {llm_name}")


def build_agent_executor(llm, tools):
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


def lookup(query: str, llm_choice: str = "gemini") -> str:
    load_dotenv()  # Ensure environment variables are loaded
    llm = get_llm(llm_choice)

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
    # Example usage; choose between 'gemini', 'ollama', or 'openai'
    linkedin_url = lookup(query="Udemy's Eden Marco Linkedin Profile", llm_choice="ollama")
    print(linkedin_url)