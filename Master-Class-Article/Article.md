# Mastering Tokens, EMbeddings, Vectors, FAISS, and MongoDB

---

## Overview

This Document focuses on five essential concepts :

- **Tokens**: The basic units into which text is split for machine processing.
- **Embeddings**: Numerical representation of tokens that capture semantic meaning.
- **Vectors**: High-dimensional arrays generated from embeddings, used for comparing and computing similarities.
- **FAISS**: A library for fast and efficient similarity search over large collections of vectors.
- **MongoDB**: A NoSQL database used to store text, metadata, and references to vector data.

Understanding how these componenets work together helps in building applications involving semantic search, text similarity, and efficient data retrieval.


---

## Table of Contents

1.[Tokens](#1-tokens)
2.[Embeddings](#2-embeddings)
3.[Vectors](#3-vectors)
4.[FAISS - Similarity Search](#4-faiss---similarity-search)
5.[MongoDB](#5-mongodb)
6.[Combined workflow](#6-combined-workflow)
7.[Sample Use Case](#7-sample-use-case)
8.[Conclusion](#8-conclusion)

---------------------------------------------------------------------------------

## 1. Tokens

**Definition:**
Tokens are the smallest meaningful units into which text is broken diwn before ut can be processed by machines.

IN Natural Language Processing (NLP), Tokenization is the first step where raw text is split into parts such as :

- **Words** -> '"The cat sat"' -> '["The", "cat", "sat"]'
- **Subwords** -> '"unhappiness"' -> '["un", "happi", "ness"]'
- **Characters** -> '"Hi" -> '["H", "i"]'

**Why Tokenization is important:**

- Enables models to handle text more efficiently
- Reduces complexity by simplifying input 
- Helps in creating embeddings from textual data

**Example in Python:**
'''python
from nltk.tokenize import word_tokenize

text = "Natural Language Processing is fun!"
tokens = word_tokenize(text)
print(tokens) # ['Natural', 'Language', 'Processing', 'is', 'fun', '!']

--- 

### Knowledge Check: Tokens

1. **What is tokenization, and ehy is it needs in NLP?**
2. **List three types of tokenization with examples.**
3. **What is the difference between word-level and subword-level.**
4. **Which type of tokenization is used by models like GPT and Llama.**
5. **Can tokenization affect the performance of an NLP model? How?**