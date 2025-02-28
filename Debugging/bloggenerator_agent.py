from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")






llm=ChatGroq(model="qwen-2.5-32b")
load_dotenv()

class State(TypedDict):
    topic: str
    title: str
    blog: str
    finalblog: str

# Define Nodes

def titleagent(state: State):
    """LLM call to generate title"""
    msg=llm.invoke(
        "<instruction>"
        f"You are an intelligent blog title generator. Your task is to create catchy, engaging,and relevant single title based on the {state['topic']} provided to you \n" + \
        "Ensure that the titles are concise, informative, and tailored to attract readers' attention. Aim for creativity while maintaining clarity and relevance to the topic at hand."
        "</instruction>"
        )
    return {"title": msg.content}

def blogagent(state: State):
    """LLM call to generate blog"""
    blog=llm.invoke(
        "<instruction>"
        f"You are an intelligent blog content generator. Your task is to create a blog content based on the {state['topic']} provided to you \n" + \
        "Ensure that the blog is informative, engaging, and tailored to attract readers' attention. Aim for clarity, depth, and engagement while maintaining a high level of quality and accuracy."
        "</instruction>"
        )
    return {"blog": blog.content}

def finalblogagent(state: State):
    """Combine the title and blog into a single output"""

    combined = f"Here's a title and blog about {state['topic']}!\n\n"
    combined += f"Title:\n{state['title']}\n\n"
    combined += f"Blog:\n{state['blog']}\n\n"
    return {"finalblog": combined}

def make_default_graph():
    """Make a simple LLM agent"""
    graph_workflow = StateGraph(State)
    graph_workflow.add_node("titleagent", titleagent)
    graph_workflow.add_node("blogagent", blogagent)
    graph_workflow.add_node("finalblogagent", finalblogagent)
    graph_workflow.add_edge(START, "titleagent")
    graph_workflow.add_edge(START, "blogagent")
    graph_workflow.add_edge("titleagent", "finalblogagent")
    graph_workflow.add_edge("blogagent", "finalblogagent")
    graph_workflow.add_edge("finalblogagent", END)

    agent = graph_workflow.compile()
    return agent

agent=make_default_graph()