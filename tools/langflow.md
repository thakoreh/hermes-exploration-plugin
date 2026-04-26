---
id: langflow
name: Langflow
description: Visual flow-based editor for building RAG and LLM pipelines. Drag components, connect them, iterate fast. Exports to LangChain, llama_index, or standalone Python.
category: llm-app-builder
url: https://langflow.org
pricing: free
alternatives:
  - dify
  - flowise
  - langchain
quality_score: 8.4
discovery_context: Visual RAG builder for non-engineers on the team who need to iterate on retrieval pipelines
discovered_by: hermes-mlops
discovered_at: 2026-04-25
last_verified: 2026-04-25
flags:
  - open-source
  - has-api
  - has-free-tier
  - has-visual-builder
Best for: RAG pipelines, LLM orchestration, visual prototyping of AI flows
Free: 100 AI requests/mo on cloud, self-hosted free
Install: pip install langflow OR docker run langflowai/langflow
---

# Langflow

Langflow is a visual, flow-based editor for building LLM applications. Think of it as a visual programming environment for AI — drag components, connect them, see results immediately. Export to production Python (LangChain, llama_index) or deploy as-is.

## Components

- **Loaders**: File, URL, API, Database, Vector store
- **Prompts**: Prompt editor with variable injection
- **Models**: OpenAI, Anthropic, Ollama, Azure, Google, AWS Bedrock
- **Vector Stores**: Pinecone, Weaviate, Chroma, FAISS, Qdrant
- **Chains**: RAG, conversational, agentic, multi-modal
- **Memory**: Buffer, summary, entity memory
- **Output**: JSON, markdown, file, API response

## Key Workflows

### RAG Pipeline
```
File Loader → Text Splitter → Embeddings → Vector Store → LLM → Output
                     ↑                              ↑
              (retrieved docs)              (user query)
```

### Conversational Agent
```
Chat Input → Memory → Prompt → LLM → Tool Use → Output
                              ↑
                       (external API / DB)
```

## Deployment

- **Cloud**: langflow.org (free tier)
- **Self-hosted**: Docker one-liner, full customization
- **Export**: Generate Python/LangChain code to embed in your app

## Best For

- Rapid prototyping of RAG systems
- Non-engineers building AI flows
- Visual debugging of retrieval pipelines
- Testing different embedding/chunking strategies
