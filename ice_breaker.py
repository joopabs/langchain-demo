from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
from langchain.schema import StrOutputParser
from dotenv import load_dotenv
from rich import print

def create_prompt_template():
    summary_template = """
        Given the following information about a person:
        {information}

        Please create the following:
        1. A short summary of the person.
        2. Two interesting facts about them.
    """
    return PromptTemplate.from_template(summary_template)

def create_langchain_pipeline(llm):
    prompt_template = create_prompt_template()
    output_parser = StrOutputParser()
    return prompt_template | llm | output_parser

def process_information_streamed(information):
    """Processes the given information using the LangChain pipeline, streaming the result."""
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    # llm = ChatOllama(model="llama3")
    prompt_template = create_prompt_template()
    chain = prompt_template | llm

    for chunk in chain.stream(input={"information": information}):
        if hasattr(chunk, 'content'):
            print(chunk.content, end="", flush=True)

def main():
    """Main function to execute the information processing."""
    print("Hello Langchain!")

    information = """
    Elon Reeve Musk (June 28, 1971) is a businessman known for his key roles in Tesla, Inc., SpaceX, and Twitter (which he rebranded as X). Since 2025, he has been a senior advisor to United States president Donald Trump and the de facto head of the Department of Government Efficiency (DOGE). Musk is the wealthiest person in the world; as of March 2025, Forbes estimates his net worth to be US$343 billion.

    Born to a prominent family in Pretoria, South Africa, Musk emigrated to Canada in 1989 and acquired its citizenship though his mother. He moved to the U.S. and graduated from the University of Pennsylvania before moving to California to pursue business ventures. In 1995, Musk co-founded the software company Zip2. After its sale in 1999, he co-founded X.com, an online payment company that later merged to form PayPal, which was acquired by eBay in 2002 for $1.5 billion. That year, Musk also became a U.S. citizen.

    In 2002, Musk founded SpaceX and became its CEO and chief engineer. The company has since led innovations in reusable rockets and commercial spaceflight. In 2004, Musk joined Tesla, Inc., as an early investor, and became its CEO and product architect in 2008; it has become a market leader in electric vehicles. In 2015, he co-founded OpenAI to advance artificial intelligence research, but left its board in 2018. In 2016, Musk co-founded Neuralink, a company focused on brain–computer interfaces, and in 2017 launched the Boring Company, which aims to develop tunnel transportation. Musk was named Time magazine's Person of the Year in 2021. In 2022, he acquired Twitter, implementing significant changes and rebranding it as X in 2023. In January 2025, he was appointed head of Trump's newly created DOGE.

    Musk's political activities and views have made him a polarizing figure. He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation and promoting conspiracy theories. His acquisition of Twitter (now X) was controversial due to a subsequent increase in hate speech and the spread of misinformation on the service. He has engaged in political activities in several countries, including as a vocal and financial supporter of Trump. Musk was the largest donor in the 2024 U.S. presidential election and is a supporter of global far-right figures, causes, and political parties.
    """

    result = process_information_streamed(information)
    print(result)

if __name__ == "__main__":
    load_dotenv()
    main()