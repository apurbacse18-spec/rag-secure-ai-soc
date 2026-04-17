# RAG Secure AI SOC

This project builds a Retrieval-Augmented Generation (RAG) based AI system for SOC knowledge assistance and evaluates its security using Wazuh, Suricata, MITRE ATT&CK, MITRE ATLAS, and forensic validation tools.

## Features
- FastAPI-based RAG application
- Structured JSON logging
- Document loading and chunking
- Vector search with FAISS
- Retrieval from SOC knowledge documents

## Current Status
- Project repository created
- Virtual environment configured
- FastAPI app running
- Initial RAG retrieval pipeline implemented

## Run the App
```bash
uvicorn rag_app.main:app --reload