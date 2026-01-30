# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: NanoGraphRAG 工具函数
"""

import numpy as np
import tiktoken


def get_tokenizer(model: str = "gpt-4o-mini"):
    """获取 tokenizer"""
    return tiktoken.encoding_for_model(model)


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 100,
    model: str = "gpt-4o-mini"
) -> list[dict]:
    """
    按 token 数量分块
    
    Returns:
        [{"content": str, "index": int, "tokens": int}, ...]
    """
    tokenizer = get_tokenizer(model)
    tokens = tokenizer.encode(text)
    
    chunks = []
    start = 0
    index = 0
    
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        
        chunks.append({
            "content": chunk_text,
            "index": index,
            "tokens": len(chunk_tokens)
        })
        
        start = start + chunk_size - overlap
        index += 1
    
    return chunks


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """计算两个向量的余弦相似度"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(np.dot(v1, v2) / (norm1 * norm2))


def batch_cosine_similarity(query_vec: list[float], vectors: list[list[float]]) -> np.ndarray:
    """
    批量计算余弦相似度 (numpy 加速)
    
    Args:
        query_vec: 查询向量 [dim]
        vectors: 候选向量列表 [[dim], [dim], ...]
    
    Returns:
        相似度数组 [n_vectors]
    """
    if not vectors:
        return np.array([])
    
    query = np.array(query_vec)
    matrix = np.array(vectors)
    
    # 归一化
    query_norm = query / (np.linalg.norm(query) + 1e-10)
    matrix_norms = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-10)
    
    # 批量点积
    similarities = matrix_norms @ query_norm
    
    return similarities


def top_k_similar(
    query_vec: list[float], 
    keys: list[str], 
    vectors: list[list[float]], 
    top_k: int = 10
) -> list[tuple[str, float]]:
    """
    批量检索 top-k 最相似的向量
    
    Args:
        query_vec: 查询向量
        keys: 向量对应的 key 列表
        vectors: 向量列表
        top_k: 返回数量
    
    Returns:
        [(key, score), ...] 按相似度降序排列
    """
    if not vectors:
        return []
    
    scores = batch_cosine_similarity(query_vec, vectors)
    
    # 获取 top-k 索引
    k = min(top_k, len(scores))
    top_indices = np.argsort(scores)[::-1][:k]
    
    return [(keys[i], float(scores[i])) for i in top_indices]
