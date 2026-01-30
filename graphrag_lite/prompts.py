# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: NanoGraphRAG Prompt 模板
"""

# 实体和关系提取
ENTITY_EXTRACTION_PROMPT = """You are a knowledge graph expert. Extract entities and relations from the text below.

Text:
{text}

Output format (one per line):
- Entity: entity||name||type||description
- Relation: relation||source||target||keywords||description

Entity types: person, organization, location, event, concept, object, etc.
Keywords should be core words describing the relation.

Output:"""


# RAG 回答生成
RAG_RESPONSE_PROMPT = """Answer the question based on the retrieved knowledge below.

Knowledge:
{context}

Question: {query}

Instructions:
- Answer based only on the provided knowledge
- If the knowledge is insufficient, say so
- Be concise and accurate
- Use markdown formatting
- Ouput asnwer in the same language as the question

Answer:"""
