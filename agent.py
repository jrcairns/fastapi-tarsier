from langchain.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

async def setup_agent(tools):
    template = """
    You are a web interaction agent. Use the read page tool to understand where you currently are. 
    You will be passed in OCR text of a web page where element ids are to the left of elements. 

    You have access to the following tools:
    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    ... (this Thought/Action/Action Input can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    These were previous tasks you completed:

    Begin!

    Question: {input}
    {agent_scratchpad}"""
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=50,  # Increase the maximum number of iterations
        max_execution_time=300,
    )

    return agent_chain