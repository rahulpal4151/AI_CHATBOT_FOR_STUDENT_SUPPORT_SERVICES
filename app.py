
from flask import Flask, render_template, jsonify, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = download_embeddings()

index_name = "studentchatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# 1. Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0.3, 
    max_tokens=500,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# 2. Base Retriever (Pinecone database connection - k ki value 10 ya 15 safe rahegi)
base_retriever = docsearch.as_retriever(search_kwargs={"k": 20})

# 2.5 Bullet-Proof Safe Retriever Function (Jo dictionary se search text nikalegi)
def safe_retrieve(chain_input):
    # Agar chain se dictionary aa rahi hai, toh "input" key se query string nikalein
    if isinstance(chain_input, dict):
        search_query = chain_input.get("input", "")
    else:
        search_query = str(chain_input)
        
    # Base retriever ko ab hamesha sirf string milegi
    docs = base_retriever.invoke(search_query)
    
    safe_docs = []
    for doc in docs:
        if isinstance(doc, dict):
            safe_docs.append(Document(
                page_content=doc.get("page_content", "") or doc.get("text", str(doc)),
                metadata=doc.get("metadata", {})
            ))
        elif hasattr(doc, "page_content"):
            safe_docs.append(doc)
        else:
            safe_docs.append(Document(page_content=str(doc)))
    return safe_docs

safe_retriever_chain = RunnableLambda(safe_retrieve)

# 3. Safe formatting function
def format_docs(docs):
    clean_texts = []
    for doc in docs:
        content = doc.page_content
        if isinstance(content, str):
            content = content.replace("\n", " ")
        clean_texts.append(content)
    return "\n\n".join(clean_texts)

# 4. Prompt Setup
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 5. Fixed Modern LCEL Pipeline
rag_chain = (
    {
        "context": safe_retriever_chain | format_docs, 
        "input": lambda x: x["input"] if isinstance(x, dict) else x
    }
    | prompt
    | llm
    | StrOutputParser()
)

print("Super Safe Modern LCEL RAG Chain ready! 🚀")


@app.route('/')
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("User Message:", msg)
    
    # Chain ko call karein (Modern LCEL direct string return karega)
    response = rag_chain.invoke({"input": msg})
    
    # Direct response ko print karein, dictionary key mat lagayein!
    print("Response : ", response)
    
    return str(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)