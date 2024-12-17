from PyPDF2 import PdfReader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve database credentials
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Initialize LangChain's OpenAI embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2")


# Define the table and embedding dimensions
TABLE_NAME = "sentences_lang"
EMBEDDING_DIM = 1536  # OpenAI's text-embedding-ada-002 outputs 1536 dimensions


# Initialize the Postgres vector database
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=TABLE_NAME,
    connection=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=disable",
    use_jsonb=True,
)


def insert_pdf_to_db(pdf_path):
    # Read the PDF content
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Split text into sentences
    sentences = [line.strip() for line in text.split("\n") if line.strip()]

    # Add sentences and embeddings to the vector database
    vector_store.add_texts(texts=sentences)
    print("PDF data inserted successfully.")


def query_similar_sentences(query_sentence, limit=5):
    # Embed the query sentence
    query_embedding = embeddings.embed_query(query_sentence)
    print(query_sentence)
    # Perform similarity search
    results = vector_store.similarity_search_by_vector(
        query_embedding, k=limit)

    for res in results:
        print(res)

    # Return results
    return [{"sentence": res.page_content} for res in results]

# Example usage
# query = "AI is transforming the world."
# matches = query_similar_sentences(query, limit=5)
# print(matches)
