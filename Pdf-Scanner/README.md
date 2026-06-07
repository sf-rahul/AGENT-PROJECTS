# PDF Scanner

PDF Scanner is an AI-powered chat application that allows users to interact with a Large Language Model (LLM) for general conversations and PDF document analysis. Users can ask general questions, upload PDF documents, and request summaries or information extraction from the uploaded files.

## Features

* Interactive AI chat interface
* General-purpose question answering
* PDF document reading and text extraction
* PDF content summarization
* Question answering based on document content
* Local LLM support using Ollama

## Project Structure

```text
Agentic-AI/
└── Agentic-Projects/
    └── pdf-scanner/
        ├── app.py
        └── README.md
```

## Prerequisites

Before running the application, install:

* Python 3.10+
* Ollama
* UV
* OpenAI Python Client

## Installation

### Navigate to the Project

```bash
cd Agentic-AI/Agentic-Projects/pdf-scanner
```

### Install Dependencies

```bash
uv sync
```

### Start Ollama

Pull and run your preferred model.

Example:

```bash
ollama pull qwen3:8b
ollama serve
```

## Running the Application

From the `pdf-scanner` directory:

```bash
uv run app.py
```

## Usage

### General Chat

Ask questions directly to the LLM.

Examples:

* What is Artificial Intelligence?
* Explain Salesforce Agentforce.
* Write a Python function to sort a list.

### PDF Reading

Upload a PDF and ask questions such as:

* Read this PDF.
* Summarize the document.
* What are the key points?
* Extract important information from this file.

## Technology Stack

* Python
* Ollama
* OpenAI-Compatible Client
* UV

## Future Enhancements

* Support for DOCX and TXT files
* Multi-document analysis
* Chat history persistence
* RAG-based retrieval
* Source citations
* Multiple model selection

## License

This project is intended for educational and experimentation purposes within the Agentic-AI project collection.
