from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.agents import Tool, create_react_agent, AgentExecutor, tool
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    template = """given the full name {name_of_person} I want you get me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url
