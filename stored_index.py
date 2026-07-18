from src.helper import load_all_files, filter_to_minimal_docs, text_split, download_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os



load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data = load_all_files("data")            
minimal_docs = filter_to_minimal_docs(extracted_data)
texts_chunk = text_split(minimal_docs)
embeddings = download_embeddings()

# pinecone_api_key = PINECONE_API_KEY
# pc = Pinecone(api_key=pinecone_api_key)

pc = Pinecone(api_key="your_pinecone_api_key")

index_name = "studentchatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )


# Embed each chunk and upsert the embeddings into your Pinecone index
docsearch = PineconeVectorStore.from_documents(
    documents=texts_chunk,
    embedding=embeddings,
    index_name=index_name
)
