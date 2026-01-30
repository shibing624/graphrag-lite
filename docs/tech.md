# NanoGraphRAG 技术文档

## 项目概述

NanoGraphRAG 是一个极简的 GraphRAG 实现，约 600 行 Python 代码，专为教学和学习设计。

## 与 nano-graphrag 对比

| 维度 | **NanoGraphRAG** | **nano-graphrag** |
|------|------------------|-------------------|
| 代码量 | ~600 行 | ~1100 行 |
| 依赖 | openai, numpy, tiktoken, loguru | networkx, nano-vectordb 等 |
| LLM | 仅 OpenAI | 可插拔 (OpenAI, Ollama, DeepSeek 等) |
| 向量存储 | 内存 + JSON | nano-vectordb, hnswlib, milvus, faiss |
| 图存储 | 内存 + JSON | networkx, Neo4j |
| 异步支持 | ❌ | ✅ |
| 定位 | **教学/学习** | 生产级 |

## 核心优化

### 1. 批量 Embedding
```python
def _get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
    """一次 API 请求获取多个文本的 embedding"""
```
减少 API 调用次数，提升插入速度。

### 2. LLM 响应缓存
```python
# MD5 hash 作为 key，缓存到 llm_cache.json
cache_key = hashlib.md5(prompt.encode()).hexdigest()
```
相同 prompt 直接返回缓存结果，避免重复调用。

### 3. NumPy 加速向量检索
```python
def top_k_similar(query_vec, keys, vectors, k):
    """NumPy 批量计算 cosine similarity"""
    matrix = np.array(vectors)
    query = np.array(query_vec)
    similarities = matrix @ query / (norms * query_norm)
```
替代逐个计算，大幅提升检索速度。

### 4. 流式输出
```python
def query(self, question, stream=True):
    for chunk in response:
        yield chunk.choices[0].delta.content
```

## 查询模式

| 模式 | 原理 | 适用场景 |
|------|------|----------|
| `local` | 实体向量检索 → 获取邻居关系 | 特定实体问题 |
| `global` | 关系向量检索 → 获取关联实体 | 关系类问题 |
| `mix` | 实体 + 关系 + 原始文本块 | **推荐，综合效果最佳** |
| `naive` | 仅文本块检索 (传统 RAG) | 对比基线 |

## 项目结构

```
nanographrag/
├── __init__.py      # 包入口，版本 0.1.0
├── core.py          # 核心实现 (~620 行)
├── prompts.py       # 实体/关系提取提示词
├── utils.py         # 工具函数 (分块、向量检索)
├── pyproject.toml   # PyPI 发布配置
├── README.md        # 项目文档
└── LICENSE          # MIT 许可证
```

## PyPI 发布

```bash
cd nanographrag
pip install build twine
python -m build
twine upload dist/*
```

## 使用示例

```python
from nanographrag import NanoGraphRAG

graph = NanoGraphRAG(
    storage_path="./data",
    api_key="sk-xxx",
)

# 插入文档
graph.insert("文档内容...")

# 查询 (推荐 mix 模式)
answer = graph.query("问题?", mode="mix")

# 流式输出
for chunk in graph.query("问题?", stream=True):
    print(chunk, end="")
```

## 设计理念

**不与 nano-graphrag 卷功能/性能，专注极简教学**：
- 单文件即可理解全部逻辑
- 零配置，开箱即用
- 10 分钟看懂 GraphRAG 原理
