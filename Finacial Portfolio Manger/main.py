from src.model import llm

if __name__ == "__main__":
    llm = llm()

    question = "what is bend gate scam?"
    response = llm.invoke(question)

    print(response.content)