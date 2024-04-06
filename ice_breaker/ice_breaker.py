from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser.output_parsers import person_intel_parser, PersonIntel
from typing import Tuple
import asyncio


## Async
async def create_model():
    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    3. A topic that may interest them
    4. 2 creative Ice breakers to open a conversation with them
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )
    output_parser = StrOutputParser()

    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
    chain = summary_prompt_template | llm | output_parser
    return chain

async def generate_response(model, information):
    async for chunk in model.astream(input={"information": information}):
        yield chunk


async def ice_breaker(name: str):
    # linkedin_profile_url = linkedin_lookup_agent(name=name)

    linkedin_information = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/mario-t-3538aa205/"
        # linkedin_profile_url=linkedin_profile_url
    )
    model: RunnableSequence = await create_model()

    # response = model.invoke(input={"linkedin_information": linkedin_information})

    async for chunk in generate_response(model, linkedin_information):
        # print(chunk, end="")
        yield {"chunk": chunk, "url": linkedin_information.get("profile_pic_url")}


async def main(name):
    info = ""
    async for chunk in ice_breaker(name):
        info += chunk["chunk"]
    return info, chunk["url"]



## Sync
def create_model_sync() -> LLMChain:
    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    3. A topic that may interest them
    4. 2 creative Ice breakers to open a conversation with them
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
    output_parser = person_intel_parser
    chain = summary_prompt_template | llm | output_parser
    # chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    return chain
def ice_breaker_sync(name: str) -> Tuple[PersonIntel, str]:
    linkedin_profile_url = linkedin_lookup_agent(name=name)

    linkedin_information = scrape_linkedin_profile(
        # linkedin_profile_url="https://www.linkedin.com/in/mario-t-3538aa205/"
        linkedin_profile_url=linkedin_profile_url
    )
    model: RunnableSequence = create_model_sync()

    response = model.invoke({"information": linkedin_information})
    
    return (response, linkedin_information.get("profile_pic_url"))

if __name__ == "__main__":
    load_dotenv()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(main())
    print(ice_breaker_sync("Mario")[0].summary)
