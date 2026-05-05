from src.chain import build_graph
from src.agents import stock_picker

if __name__ == "__main__":

    question = """
    what is a good investmetn stragety for a 30 year
    old moderate risk investro with 1000 to invest for
    30 years?"""

    workflow = build_graph()
    response = workflow.invoke({
        "user_input": question,
        "chat_history": [],
        "stock_picker_history": [],
        "iterations": 0,
        "iterations_stock_picker": 0,
        "risk_free_rate": 0.02
    })

    print(response["filtered_stocks"])