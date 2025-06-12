# CodeAmigo
CLI chatbot to aid with coding and analysis

This is a **local, intelligent code analysis assistant** powered by LLMs (Large Language Models) designed to help you **analyze**, **understand**, and **ask questions about your codebases**—whether Java, Python, Gradle, YAML, or others.

## Features

-  Analyze **multiple programming languages**: Java, Python, Gradle, YAML, properties, Markdown, etc.
-  Search code contextually using embeddings + **FAISS vector store**
-  Powered by **local LLMs** via [Ollama](https://ollama.com/)
-  Supports **CodeLlama 7B/13B** and other models for **code reasoning**
-  Automatically skips binaries, compiled files, and unnecessary folders
-  Modular and customizable for various development workflows

---

## Setup Instructions

### Install Ollama
Install Ollama for running local models: https://ollama.com/download

### Pull Models
```bash
ollama pull codellama:7b
ollama pull codellama:13b
```

### Install requirements.txt
```bash
pip install -r requirements.txt
```

### Run the Chatbot
```bash
python CodeAmigo.py
```
1. Provide the inputs when prompted.
2. Type 'exit' to quit.
3. Switch between models if needed.