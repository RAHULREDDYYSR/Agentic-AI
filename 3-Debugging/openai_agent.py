from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from pprint import pprint
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool


class State(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]


model = ChatOpenAI(model='gpt-4.1-nano')

def make_default_graph():
    graph_workflow=StateGraph(State)

    def call_model(state:State):
        return {'messages':[model.invoke(state['messages'])]}
    
    graph_workflow.add_node('agent', call_model)
    graph_workflow.add_edge('agent',END)
    graph_workflow.add_edge(START,'agent')

    agent = graph_workflow.compile()
    return agent

agent = make_default_graph()