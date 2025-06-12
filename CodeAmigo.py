# Minimal prototype for an in-house chatbot that understands code

import os
import string 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from datetime import datetime

# ---- Step 1: Load Java code ----
def load_java_files(directory):
    java_files = []
    print('🔍 Scanning directory:', directory)
    for root, _, files in os.walk(directory):
        print('📁 Current root:', root)
        for file in files:
            print('📄 Found file:', file)
            if file.endswith(".java"):
                path = os.path.join(root, file)
                print('✅ Loading Java file:', path)
                with open(path, 'r', encoding='utf-8') as f:
                    java_files.append(f.read())
    return java_files

SKIP_EXTENSIONS = {
    '.class', '.jar', '.exe', '.dll', '.so', '.bin', '.pyc', '.pyo',
    '.zip', '.tar', '.gz', '.7z', '.png', '.jpg', '.jpeg', '.gif',
    '.bmp', '.ico', '.mp4', '.mp3', '.wav', '.avi', '.mov',
    '.pdf', '.ttf', '.otf', '.woff', '.woff2', '.mf', '.git', '.gitignore', '.bat', '.gitattributes'
}

SKIP_DIRECTORIES = {'.idea', '.git', '.gradle', 'build', 'node_modules', '__pycache__'}

def load_all_text_files(directory):
    source_files = []
    print('🔍 Scanning directory:', directory)
    for root, dirs, files in os.walk(directory):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        #print('📁 Current root:', root)
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in SKIP_EXTENSIONS:
                #print(f"⛔ Skipping file due to extension: {file}")
                continue
            #print('📄 Found file:', file)
            file_path = os.path.join(root, file)
            try:
                print('✅ Loading file:', file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Basic heuristic: ignore binary files
                    if any(c not in string.printable for c in content[:100]):
                        #print(f"⚠️ Skipping likely binary content in: {file}")
                        continue
                    source_files.append(content)
            except Exception as e:
                continue
    return source_files

# ---- Step 2: Split and embed ----

def embed_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.create_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

# ---- Step 3: Set up LLM (Ollama must be running) ----

def get_ollama_llm():#use model orchestration
    return OllamaLLM(model="codellama:7b")
    #return OllamaLLM(model="codellama:13b") #slow but in depth knowledge
    #return OllamaLLM(model="llama3.2:latest") #fast but average quality

# ---- Step 4: QA Bot ----

def build_bot(vectorstore):
    llm = get_ollama_llm()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True
    )
    return qa_chain

# ---- Step 5: Run QA loop ----

def chat_loop(qa_chain):
    print("\n🔍 Ask me about your Java microservice. Type 'exit' to quit.\n")
    while True:
        query = input("You: ")
        startTime = datetime.now()
        if query.lower() in ["exit", "quit"]:
            break
        #response = qa_chain.invoke({"query": query})
        #print(f"Bot: {response}\n")
        response = qa_chain.invoke(query)
        # If response is a dict (like in RetrievalQA with `return_source_documents=True`)
        if isinstance(response, dict):
            print("\n🧠 Answer:")
            print(response.get("result", "No result found."))

            #print("\n📄 Source(s):")
            #for i, doc in enumerate(response.get("source_documents", []), start=1):
                #print(f"\n--- Document {i} ---")
                #print(doc.page_content.strip())
        else:
            print(f"\nBot: {response}")
        print("\n------------------------------------------------\n"+"Response Time: " + str(datetime.now()-startTime))    
        print("\n================================================\n")


# ---- Main ----
if __name__ == "__main__":
    SERVICE_DIR = "C:/Users/jayak/Code/Java/Chatbot_Analysis"  # Update this path as needed
    #docs = load_java_files(SERVICE_DIR)
    docs = load_all_text_files(SERVICE_DIR)
    if not docs:
        print("No Java files found. Please check your path.")
        exit(1)

    vectorstore = embed_documents(docs)
    qa_bot = build_bot(vectorstore)
    chat_loop(qa_bot)