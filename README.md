# Student Support Chatbot

## How to run?

### STEP 01- Create and activate a conda environment
```bash
conda create -n medibot python=3.10 -y
```

```bash
conda activate medibot
```

### STEP 02- Install the requirements

```bash
pip install -r requirements.txt
```

### STEP 03- Setup Environment Variables

Create a .env file in the root directory and add your credentials as follows:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GROQ_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### STEP 04- Ingest Data to Vector Database

Run the following command to chunk the documents, generate embeddings, and store them into Pinecone:

```bash
python stored_index.py
```

### STEP 05- Run the Application

```bash
python app.py
```

Now, open your browser and navigate to:

```bash
http://localhost:8080/
```



### Techstack Used:

- **Language**: Python
- **Framework:** Flask
- **LLM Orchestration:** LangChain (LCEL)
- **Large Language Model:** Llama 3.1 (via Groq Cloud API)
- **Vector Database:** Pinecone
- **Embeddings Model:** HuggingFace (sentence-transformers/all-MiniLM-L6-v2)

