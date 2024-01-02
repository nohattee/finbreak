from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from langchain.tools import E2BDataAnalysisTool, DuckDuckGoSearchRun

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="")
lc_tools = [E2BDataAnalysisTool(api_key=''), DuckDuckGoSearchRun()]

prompt = hub.pull("hwchase17/react")
prompt = prompt.partial(
    tools=render_text_description(lc_tools),
    tool_names=", ".join([t.name for t in lc_tools]),
)

llm_with_stop = llm.bind(stop=["\nObservation"])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_stop
    | ReActSingleInputOutputParser()
)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=lc_tools, verbose=True)

a = agent_executor.invoke(
    {
        "input": "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
    }
)

print(a)