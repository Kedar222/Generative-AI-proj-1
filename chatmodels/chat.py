from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9)

print("chosse you model:. Angry AI 1. Funny AI 2. Sad AI 3")

choice = int (input("Enter your choice: "))

if choice == 1:
      mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif choice == 2:
      mode ="You are a very funny  AI agent. You respond with humor and jokes."
elif choice == 3:
      mode = "You are an sad AI agent. you respond with heartborken person"

messages=[
      SystemMessage(content=mode)
]

print("--------------------- type 0 to exit the chatbot----------------------") 

while True:
    
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))

    if prompt == "0":
            break 
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bot:",response.content)


print(messages)