from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from third_parties.linkedin import scrape_linkedin_profile
import asyncio


async def create_model():
    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    output_parser = StrOutputParser()

    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    chain = summary_prompt_template | llm | output_parser
    return chain


async def generate_response(model, information):
    async for chunk in model.astream(input={"information": information}):
        yield chunk


async def main():
    information = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/mario-t-3538aa205/"
    )
    
    model: RunnableSequence = await create_model()

    # response = model.invoke(input={"information": information})
    async for chunk in generate_response(model, information):
        print(chunk, end="")


if __name__ == "__main__":
    load_dotenv()
    print("Hello Langchain")

    asyncio.run(main())
