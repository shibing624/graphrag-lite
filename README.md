# GraphRAG-Lite

<p align="center">
  <img src="https://github.com/shibing624/graphrag-lite/blob/main/docs/logo.svg" alt="GraphRAG-Lite Logo" width="400">
</p>

<p align="center">
  <b>Minimal GraphRAG implementation in ~600 lines of Python code.</b>
</p>

<p align="center">
  <a href="https://badge.fury.io/py/graphrag-lite"><img src="https://badge.fury.io/py/graphrag-lite.svg" alt="PyPI version"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0"></a>
  <a href="https://github.com/shibing624/graphrag-lite/blob/main/README.md"><img src="https://img.shields.io/badge/wechat-group-green.svg?logo=wechat" alt="Chat Group"></a>
</p>

<p align="center">
  <a href="https://github.com/shibing624/graphrag-lite/blob/main/README_zh.md">中文文档</a>
</p>

GraphRAG-Lite is a lightweight, educational implementation of GraphRAG (Graph-based Retrieval-Augmented Generation). It's designed to help you understand the core principles of GraphRAG in a single afternoon.

## Features

- **Minimal**: ~600 lines of code, easy to read and understand
- **Zero Config**: Only requires OpenAI API key, no complex setup
- **4 Query Modes**: local, global, mix, naive
- **Optimized**: Batch embeddings, LLM caching, NumPy-accelerated vector search
- **Streaming**: Real-time response output support

## Installation

```bash
pip install graphrag-lite
```

Or install from source:

```bash
git clone https://github.com/shibing624/graphrag-lite.git
cd graphrag-lite
pip install -e .
```

## Quick Start

```python
import os
from graphrag_lite import GraphRAGLite

# Initialize
graph = GraphRAGLite(
    storage_path="./my_graph",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),  # Optional
)

# Insert documents
graph.insert("""
Charles Dickens wrote "A Christmas Carol" in 1843.
The story features Ebenezer Scrooge, a miserly old man,
and the ghost of his former business partner Jacob Marley.
""")

# Query
answer = graph.query("What is the relationship between Scrooge and Marley?")
print(answer)
```

## Query Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `local` | Entity → Related relations | Specific entity questions |
| `global` | Relation → Related entities | Relationship questions |
| `mix` | Entity + Relation + Text chunks | **Recommended for most cases** |
| `naive` | Text chunks only (traditional RAG) | Baseline comparison |

```python
# Different query modes
answer = graph.query("Who is Scrooge?", mode="local")
answer = graph.query("Who is Scrooge?", mode="global")
answer = graph.query("Who is Scrooge?", mode="mix")      # Recommended
answer = graph.query("Who is Scrooge?", mode="naive")
```

## Streaming Output

```python
for chunk in graph.query("Who is Scrooge?", stream=True):
    print(chunk, end="", flush=True)
```

## API Reference

### GraphRAGLite

```python
GraphRAGLite(
    storage_path: str = "./graphrag_data",  # Data storage directory
    api_key: str = None,                     # OpenAI API key
    base_url: str = None,                    # OpenAI API base URL
    model: str = "gpt-4o-mini",              # LLM model
    embedding_model: str = "text-embedding-3-small",  # Embedding model
    chunk_size: int = 1200,                  # Text chunk size
    chunk_overlap: int = 100,                # Chunk overlap
    enable_cache: bool = True,               # Enable LLM response caching
)
```

### Methods

| Method | Description |
|--------|-------------|
| `insert(text, doc_id=None)` | Insert document and build knowledge graph |
| `query(question, mode="mix", top_k=10, stream=False)` | Query the knowledge graph |
| `has_data()` | Check if data exists |
| `get_stats()` | Get statistics |
| `list_entities()` | List all entities |
| `list_relations()` | List all relations |
| `clear()` | Clear all data |

## How It Works

<p align="center">
  <img src="https://github.com/shibing624/graphrag-lite/blob/main/docs/workflow.svg" alt="GraphRAG-Lite Workflow" width="800">
</p>

1. **Insert**: Documents are chunked, entities and relations are extracted via LLM, then embedded and stored
2. **Query**: Question is used to search relevant entities/relations/chunks, context is built, LLM generates answer

## Comparison with nano-graphrag

| Feature | GraphRAG-Lite | nano-graphrag |
|---------|---------------|---------------|
| Code Size | ~600 lines | ~1100 lines |
| Dependencies | openai, numpy, tiktoken | networkx, nano-vectordb, ... |
| LLM Support | OpenAI only | Multiple (OpenAI, Ollama, etc.) |
| Vector Storage | In-memory + JSON | Multiple backends |
| Async Support | ❌ | ✅ |
| Purpose | **Educational** | Production |

GraphRAG-Lite is designed for **learning and understanding GraphRAG principles**, not for production use. If you need a production-ready solution, consider [nano-graphrag](https://github.com/gusye1234/nano-graphrag) or [LightRAG](https://github.com/HKUDS/LightRAG).

## Community & Support

*   **GitHub Issues**: Have questions or feature requests? [Submit an issue](https://github.com/shibing624/graphrag-lite/issues).
*   **WeChat**: Join our developer community! Add WeChat ID `xuming624` with note "llm" to join the group chat.

<img src="https://github.com/shibing624/graphrag-lite/blob/main/docs/wechat.jpeg" width="200" />

## License

Apache License 2.0

## Citation

If you find this project useful, please consider giving it a ⭐ on GitHub!

```bibtex
@software{graphrag-lite,
  author = {Xu Ming},
  title = {GraphRAG-Lite: Minimal GraphRAG Implementation},
  year = {2025},
  url = {https://github.com/shibing624/graphrag-lite}
}
```
