from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

llm=ChatGroq(model="qwen-2.5-32b")
load_dotenv()

# Graph state
class State(TypedDict):
    topic: str
    code : str
    reviewer : str
    release_manager : str

# Nodes
def CoderAgent(state: State):
    "Coder class to generate the code"

    msg = llm.invoke(
        """\n<instruction>:\n\n""" + \
        f"""You are a coder tasked with writing a Python code snippet based on the given '{state['topic']}'. Your task is to create a code that fulfills the requirements of the topic and adheres to best practices in Python programming based on the following criteria: \n""" + \
        """1. **Readability**: The code easy to read and understand?\n""" + \
        """2. **Adherence to Standards**: The code should follow PEP 8 or other relevant coding standards?\n""" + \
        """3. **Error Handling**: The code should not have potential errors or exceptions that are not handled?\n""" + \
        """4. **Efficiency**: The code should be efficient in terms of performance and resource usage?\n""" + \
        """5. **Maintainability**: The code structured should be in a way that is easy to maintain and extend?\n""" + \
        """</instruction>"""
        )
    return {"code": msg.content}

def PeerReviewer(state: State):
    "PeerReviewer class to review the code"

    msg = llm.invoke(f"Review the code for {state['code']}")
    return {"reviewer": msg.content}    

def ReviewerCondition(state: State):
    "Reviewer class to review the code"
    msg = llm.invoke(
        """\n<instruction>:\n\n""" + \
        f"""You are a Peer Review Agent designed to evaluate Python code for '{state['code']}' for quality and adherence to best practices. Your task is to analyze the provided code snippet and assess its quality based on the following criteria:\n""" + \
        
        """1. **Readability**: Is the code easy to read and understand?\n""" + \
        """2. **Adherence to Standards**: Does the code follow PEP 8 or other relevant coding standards?\n""" + \
        """3. **Error Handling**: Are there any potential errors or exceptions that are not handled?\n""" + \
        """4. **Efficiency**: Is the code efficient in terms of performance and resource usage?\n""" + \
        """5. **Maintainability**: Is the code structured in a way that is easy to maintain and extend?\n""" + \
        """\nAfter reviewing the code, return only 'pass' if it meets the quality standards and 'fail' if it does not"""
        """output format : Pass/Fail"""
        """</instruction>"""
            )
    return msg.content

def ReleaseManager(state: State):
    "ReleaseManager class to release the code"

    msg = llm.invoke(f"Release the code for {state['reviewer']}")
    return {"release_manager": msg.content}

def make_default_graph():
    """Make a Peer Review LLM agent"""
    workflow = StateGraph(State)

    # Add nodes
    workflow.add_node("CoderAgent", CoderAgent)
    workflow.add_node("PeerReviewer", PeerReviewer)
    workflow.add_node("ReleaseManager", ReleaseManager)

    # # Add edges to connect nodes
    workflow.add_edge(START, "CoderAgent")
    workflow.add_edge("CoderAgent", "PeerReviewer")
    workflow.add_conditional_edges("PeerReviewer", ReviewerCondition, {"Fail": "CoderAgent", "Pass": "ReleaseManager"})
    workflow.add_edge("ReleaseManager", END)

    review_graph=workflow.compile()
    return review_graph

agent=make_default_graph()