from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from langchain_core.documents import Document



# *********************************************************************#

# Extract text from PDF files

def load_all_files(data_path):
    # 1. Pehle sirf saari PDFs load karein
    pdf_loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    pdf_docs = pdf_loader.load()
    
    # 2. Fir testing ya sample data ki Markdown files load karein (.md)
    md_loader = DirectoryLoader(data_path, glob="*.md", loader_cls=TextLoader)
    md_docs = md_loader.load()
    
    # Dono ko combine karke return karein
    return pdf_docs + md_docs

# Pura data ek sath load karein
extracted_data = load_all_files("data")


# *********************************************************************#

# Minimal Extract text from PDF files
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs

minimal_docs = filter_to_minimal_docs(extracted_data)



# *********************************************************************#

# Split the documents into smaller chunks

def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk


# *********************************************************************#

# Downloading the embeddings from HuggingFace
def download_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings

embeddings = download_embeddings()
