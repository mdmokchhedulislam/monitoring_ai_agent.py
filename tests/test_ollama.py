
from langchain_ollama import ChatOllama

# Connect with local Ollama
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

response = llm.invoke(
    "You are a DevOps engineer. "
    "Explain how to check disk usage in Linux."
)

print(response.content)
