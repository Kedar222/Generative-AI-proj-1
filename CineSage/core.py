from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)




prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are CineSage, an intelligent movie information extraction assistant.

        Extract:
        - Movie Name
        - Release Year
        - Director
        - Main Cast
        - Genre
        - Plot
        - Setting
        - Main Theme
        - Music / Soundtrack
        - IMDb Rating
        - Critical Reception
        - Notable Features
        - Quick Summary

        If information is missing, write "Not mentioned".
        """
    ),
    (
        "human",
        "Extract movie information from:\n\n{paragraph}"
    )
])

chain = prompt | model

paragraph = input("Enter a movie paragraph: ")

response = chain.invoke({
    "paragraph": paragraph
})

print("\n===== CineSage: Movie Insights =====\n")
print(response.content)

print('*'*100)