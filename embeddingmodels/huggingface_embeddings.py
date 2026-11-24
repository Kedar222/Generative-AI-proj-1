from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = [
    "What is data science?",
    "What is machine learning?",
    "What is artificial intelligence?"
]


vectors = embeddings.embed_documents(texts)

print(vectors) 