from src.agents import create_strategy
from langchain_core.messages import HumanMessage

if __name__ == "__main__":

    question = """
    what is a good investmetn stragety for a 30 year
    old moderate risk investro with 10k to invest for
    30 years?"""

    response = create_strategy({
        "chat_history": [HumanMessage(content=question)]
    })

    print(response)