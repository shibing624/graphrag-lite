# NanoGraphRAG

<p align="center">
  <img src="docs/logo.svg" alt="NanoGraphRAG Logo" width="400">
</p>

<p align="center">
  <b>极简 GraphRAG 实现，约 600 行 Python 代码。</b>
</p>

<p align="center">
  <a href="https://badge.fury.io/py/nanographrag"><img src="https://badge.fury.io/py/nanographrag.svg" alt="PyPI version"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0"></a>
  <a href="https://github.com/shibing624/nanographrag/blob/main/README_zh.md"><img src="https://img.shields.io/badge/wechat-group-green.svg?logo=wechat" alt="Chat Group"></a>
</p>

<p align="center">
  <a href="https://github.com/shibing624/nanographrag/blob/main/README.md">English</a>
</p>

NanoGraphRAG 是一个轻量级、教学导向的 GraphRAG（基于图的检索增强生成）实现。设计目标是让你在一个下午内理解 GraphRAG 的核心原理。

## 特性

- **极简**: 约 600 行代码，易于阅读和理解
- **零配置**: 只需 OpenAI API 密钥，无需复杂设置
- **4 种查询模式**: local、global、mix、naive
- **优化**: 批量 Embedding、LLM 缓存、NumPy 加速向量检索
- **流式输出**: 支持实时响应输出

## 安装

```bash
pip install nanographrag
```

或从源码安装:

```bash
git clone https://github.com/shibing624/nanographrag.git
cd nanographrag
pip install -e .
```

## 快速开始

```python
import os
from nanographrag import NanoGraphRAG

# 初始化
graph = NanoGraphRAG(
    storage_path="./my_graph",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),  # 可选
)

# 插入文档
graph.insert("""
贾宝玉是《红楼梦》的主人公，与林黛玉青梅竹马。
林黛玉才华横溢，是贾母的外孙女。
薛宝钗最终嫁给了贾宝玉。
""")

# 查询
answer = graph.query("贾宝玉和林黛玉是什么关系？")
print(answer)
```

## 查询模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| `local` | 实体 → 相关关系 | 特定实体问题 |
| `global` | 关系 → 相关实体 | 关系类问题 |
| `mix` | 实体 + 关系 + 文本块 | **推荐，适用大多数场景** |
| `naive` | 仅文本块（传统 RAG） | 基线对比 |

```python
# 不同查询模式
answer = graph.query("贾宝玉是谁？", mode="local")
answer = graph.query("贾宝玉是谁？", mode="global")
answer = graph.query("贾宝玉是谁？", mode="mix")      # 推荐
answer = graph.query("贾宝玉是谁？", mode="naive")
```

## 流式输出

```python
for chunk in graph.query("贾宝玉是谁？", stream=True):
    print(chunk, end="", flush=True)
```

## API 参考

### NanoGraphRAG

```python
NanoGraphRAG(
    storage_path: str = "./nanograph_data",  # 数据存储目录
    api_key: str = None,                      # OpenAI API 密钥
    base_url: str = None,                     # OpenAI API 基础 URL
    model: str = "gpt-4o-mini",               # LLM 模型
    embedding_model: str = "text-embedding-3-small",  # Embedding 模型
    chunk_size: int = 1200,                   # 文本块大小
    chunk_overlap: int = 100,                 # 块重叠
    enable_cache: bool = True,                # 启用 LLM 响应缓存
)
```

### 方法

| 方法 | 描述 |
|------|------|
| `insert(text, doc_id=None)` | 插入文档并构建知识图谱 |
| `query(question, mode="mix", top_k=10, stream=False)` | 查询知识图谱 |
| `has_data()` | 检查是否有数据 |
| `get_stats()` | 获取统计信息 |
| `list_entities()` | 列出所有实体 |
| `list_relations()` | 列出所有关系 |
| `clear()` | 清除所有数据 |

## 工作原理

<p align="center">
  <img src="https://github.com/shibing624/nanographrag/blob/main/docs/workflow.svg" alt="NanoGraphRAG 工作流程" width="800">
</p>

1. **插入**: 文档被分块，通过 LLM 提取实体和关系，然后 Embedding 并存储
2. **查询**: 问题用于检索相关实体/关系/文本块，构建上下文，LLM 生成答案

## 与 nano-graphrag 对比

| 特性 | NanoGraphRAG | nano-graphrag |
|------|--------------|---------------|
| 代码量 | ~600 行 | ~1100 行 |
| 依赖 | openai, numpy, tiktoken | networkx, nano-vectordb, ... |
| LLM 支持 | 仅 OpenAI | 多种 (OpenAI, Ollama 等) |
| 向量存储 | 内存 + JSON | 多种后端 |
| 异步支持 | ❌ | ✅ |
| 定位 | **教学学习** | 生产级 |

NanoGraphRAG 专为 **学习和理解 GraphRAG 原理** 而设计，不适用于生产环境。如需生产级方案，请考虑 [nano-graphrag](https://github.com/gusye1234/nano-graphrag) 或 [LightRAG](https://github.com/HKUDS/LightRAG)。

## 社区与支持

*   **GitHub Issues**：有任何问题或功能请求？[提交 issue](https://github.com/shibing624/nanographrag/issues)。
*   **微信**：加入我们的开发者社群！添加微信号 `xuming624`，并备注"llm"，即可加入群聊。

<img src="https://github.com/shibing624/nanographrag/blob/main/docs/wechat.jpeg" width="200" />

## 许可证

Apache License 2.0

## 引用

如果你觉得这个项目有用，欢迎在 GitHub 上给个 ⭐！

```bibtex
@software{nanographrag,
  author = {Xu Ming},
  title = {NanoGraphRAG: Minimal GraphRAG Implementation},
  year = {2026},
  url = {https://github.com/shibing624/nanographrag}
}
```
