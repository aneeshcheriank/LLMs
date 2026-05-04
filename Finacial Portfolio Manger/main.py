from src.chain import build_graph
from langchain_core.messages import HumanMessage

if __name__ == "__main__":

    question = """
    what is a good investmetn stragety for a 30 year
    old moderate risk investro with 10k to invest for
    30 years?"""

    workflow = build_graph()
    response = workflow.invoke({
        "user_input": question,
        "chat_history": [],
        "iterations": 0
    })

    print(response)