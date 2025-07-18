# Masterclass: Understanding Tokens, Embeddings, Vectors, FAISS, and MongoDB

## Overview

This Document focuses on five essential concepts :

- **Tokens**: The basic units into which text is split for machine processing.
- **Embeddings**: Numerical representation of tokens that capture semantic meaning.
- **Vectors**: High-dimensional arrays generated from embeddings, used for comparing and computing similarities.
- **FAISS**: A library for fast and efficient similarity search over large collections of vectors.
- **MongoDB**: A NoSQL database used to store text, metadata, and references to vector data.

Understanding how these componenets work together helps in building applications involving semantic search, text similarity, and efficient data retrieval.

---

# 1. Understanding Tokens

## Section 1: What is a Token?

Tokens are the smallest meaningful units into which text is broken down before it can be processed by machines.Depending on the tokenizer, tokens can be words, sub-words, or characters.

### Examples: 
- **Words** -> '"The cat sat"' -> '["The", "cat", "sat"]'
- **Subwords** -> '"unhappiness"' -> '["un", "happi", "ness"]'
- **Characters** -> '"Hi" -> '["H", "i"]'

---

## Section 2: Tokenization in GPT Models

- Efficientlty represents rare and common words
- Breaks unknown words into known subword tokens
- Each token maps to a specific token ID

### Example:
`"unbelievable"` -> `["un", "believ", "able"]` -> `[1234, 5678, 4321]`

---

## Section 3: Why Tokenization is important:

- Enables models to handle text more efficiently
- Reduces complexity by simplifying input 
- Helps in creating embeddings from textual data

### GPT Tokenization Example:
```python
from nltk.tokenize import word_tokenize

text = "Natural Language Processing is fun!"
tokens = word_tokenize(text)
print(tokens) 

# Sample Output: 
# ['Natural', 'Language', 'Processing', 'is', 'fun', '!']
```
--- 

## Section 4: 🤖 What is a Model?
 
A **model** in programming or machine learning is a representation of a system, concept, or logic. It is used to make decisions, predictions, or structure data.
 
- In **FastAPI / Python**, a model often refers to a **Pydantic model** or a **database model** used to define the schema of data.
- In **Machine Learning (ML)**, a model is trained on data to make predictions or classifications.
 
---
 
## Section 5: 📘 What is a Language Model (LM)?
 
A **Language Model** is a type of ML model designed to understand, generate, and predict human language.
 
- Trained on large amounts of text data.
- Can perform tasks like autocomplete, translation, summarization, question answering, etc.
- Example tasks:  
  - Predict the next word in a sentence.  
  - Generate human-like responses to text input.
 
### Examples of Language Models:
| Model Name     | Developer | Description                             |
|----------------|-----------|-----------------------------------------|
| GPT-2          | OpenAI    | Autoregressive LM for text generation   |
| BERT           | Google    | Bidirectional encoder for understanding |
| RoBERTa        | Facebook  | Robust BERT variant                     |
 
---
 
## Section 6: 🧠 What is a Large Language Model (LLM)?
 
A **Large Language Model (LLM)** is a **language model** with **billions of parameters**, trained on massive datasets.
 
### Key Features of LLMs:
- Can generate paragraphs of coherent text.
- Understand context deeply.
- Can handle Q&A, summarization, code generation, etc.
 
### Examples of LLMs:
| Model        | Developer | Parameters | Notable Use                    |
|--------------|-----------|------------|--------------------------------|
| GPT-3        | OpenAI    | 175B       | Chatbots, creative writing     |
| GPT-4        | OpenAI    | ~1T (est.) | Advanced reasoning, coding     |
| LLaMA 2      | Meta      | 7B - 65B   | Open-source research           |
| Claude       | Anthropic | Proprietary| Safer conversational AI        |
 
---

## Section 7: Transformers

`Transformers` are cutting-edge deep learning architectures that have transformed the field of Natural Language Processing (NLP). Transformers rely on self-attention mechanisms, allowing them to understand context across entire sequences rather than token-by-token like RNNs. They are used in popular models like GPT, BERT...

## Transformers with GPT Tokenizer

- Provided by `Hugging Face` under transformers library.
- Pretrained with vocabulary specific to GPT2 or GPT4.
- Converts text -> tokens -> IDs

**Hugging Face** is a leading open-source AI company that provides a powerful platform for working with **natural language processing (NLP)**, **machine learning**, and **transformers-based models**. It is best known for the `transformers` library, which offers access to **state-of-the-art pre-trained models** like BERT, GPT, RoBERTa, T5, and many more.

---

## Section 8: GPT Tokenizer Source Code

```python
## Source Code

from transformers import GPT2Tokenizer
 
# Load the GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
 
# Input text
text = "Hello, my name is Surendra!"
 
# Tokenize the text
tokens = tokenizer.tokenize(text)
print("Tokens:", tokens)
 
# Convert tokens to IDs
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print("Token IDs:", token_ids)
 
# Encode full sentence with padding and truncation
encoded = tokenizer.encode_plus(
    text,
    return_tensors="pt",
    padding='max_length',
    max_length=10,
    truncation=True
)
print("Encoded input IDs:", encoded['input_ids'])

```
### Output:

- **Tokens**: ['Hello', ' , ', 'my', 'name', 'is', 'Sur', 'endra', '!']
- **Token IDs**: [15496, 11, 616, 1483, 318, 12911, 13799, 0]

### [Click Here to see more about Hugging Face](Split_Content/Hugging_face.md)
---

## Section 9: Knowledge Check: Interview Questions on Tokens

1. **What is tokenization, and why is it needs in NLP?**
2. **List three types of tokenization with examples.?**
3. **What is the difference between word-level and subword-level.?**
4. **Which type of tokenization is used by models like GPT and Llama.?**
5. **Can tokenization affect the performance of an NLP model? How?**

---

# 2.📌 Understanding Embeddings 
 
## Section 1: 🧠 What Are Embeddings?
 
Embeddings are **numerical representations of words, sentences, or documents** in a continuous vector space. These vectors capture **semantic meaning**, allowing machine learning models to understand relationships between words beyond just raw text.
 
### Example:
- The words **"king"** and **"queen"** will have similar embeddings.
- The vector operation: `embedding("king") - embedding("man") + embedding("woman") ≈ embedding("queen")`
 
---
 
## Section 2: 🧩 Why Are Embeddings Important?
 
- **Captures context & meaning** in vector form
- Makes **semantic similarity** and **clustering** possible
- Used in **search engines**, **recommendation systems**, **chatbots**, and **text classification**
- Required for **FAISS indexing** and **semantic search**
 
---
 
## Section 3: 🏗️ Types of Embeddings
 
| Type | Description |
|------|-------------
| **Word Embeddings** | Fixed vectors for each word 
| **Contextual Embeddings** | Vary by sentence context 
| **Sentence Embeddings** | Represent full sentences 
| **Document Embeddings** | Represent paragraphs or docs
 
---
 
## Section 4: 🤗 Using Hugging Face for Embeddings (with GPT and Transformers)
 
```python
from transformers import GPT2Tokenizer, GPT2Model
import torch
 
# Load GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
 
# Encode input text
text = "Natural Language Processing with GPT"
inputs = tokenizer(text, return_tensors="pt")
 
# Get hidden states (embeddings)
with torch.no_grad():
    outputs = model(**inputs)
 
# Get the last hidden state
embeddings = outputs.last_hidden_state
 
# Print the shape: [batch_size, sequence_length, embedding_dim]
print(embeddings.shape)
```

**Each token is converted into a 768-dimensional vector using GPT-2 embedding layer.**

---

## Section 5: Libraries Used:
 
- transformers: for GPT model and tokenizer
- `torch`: for handling model input/output tensors

### 🔧 `torch`
 
`torch` is the core library of **PyTorch**, an open-source deep learning framework developed by Facebook's AI Research lab. It is widely used for building and training neural networks and supports dynamic computation graphs.
 
## Section 6: ❓ Knowledge Check : Interview Questions on Embeddings 
 
1. What are embeddings and why are they important in NLP?
2. How does GPT generate embeddings from input tokens?
3. What is the role of `last_hidden_state` in GPT model output?
4. What is the difference between token IDs and embeddings?
5. How are contextual embeddings better than static embeddings?
6. What is the shape of the embeddings returned by GPT2Model?
7. How can we use GPT embeddings for semantic similarity?
8. What libraries are commonly used to extract GPT embeddings?
9. How do embeddings change with slight changes in input text?
10. How do positional embeddings work in GPT models?

---

# 3.📊 Understanding Vectors

## Section 1: What are Vectors?
 
In Natural Language Processing (NLP), **vectors** are numerical representations of text data (words, sentences, or documents). These vectors allow machines to understand and compute similarities, relationships, or perform downstream tasks such as search, classification, or clustering.
 
---

## Section 2: 🧠 How Vectors are Used?
 
Vectors are essential for:
- Capturing the **semantic meaning** of words or phrases
- Comparing **textual similarity** using distance metrics (cosine, Euclidean)
- Feeding into models like FAISS for fast retrieval
- Clustering or grouping similar documents
- Input to classifiers or other ML models
 
---

## Section 3: 🔄 From Tokens to Vectors (GPT Workflow)
 
1. **Tokenization** – Text is split into tokens using a GPT tokenizer (e.g., `GPT2Tokenizer`).
2. **Embedding** – Tokens are converted into dense vectors via the GPT model (`GPT2Model`).
3. **Vector Output** – Output from GPT includes hidden states which are high-dimensional vectors representing context-aware meaning.
 
### Example flow:

```python
from transformers import GPT2Tokenizer, GPT2Model
import torch
 
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
 
text = "Machine learning is powerful"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
vectors = outputs.last_hidden_state  # Shape: [1, seq_len, hidden_size]

```

**These vectors are often obtained from pre-trained models like GPT using their hidden states (embeddings).**
 
---
 
## Section 4: 🧩 Types of Vectors
 
1. **Word Vectors** – Represent individual words (e.g., using Word2Vec, GloVe).
2. **Sentence Vectors** – Represent full sentences (e.g., Sentence Transformers, GPT outputs).
3. **Document Vectors** – Represent large chunks of text or full documents.
4. **Contextual Vectors** – Represent words in their specific context (e.g., via GPT or BERT).
 
---
 
## Section 5: 🧠 Sample Code: Generate Sentence Vector using GPT
 
```python
from transformers import GPT2Tokenizer, GPT2Model
import torch
 
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
 
text = "Vectors are powerful in NLP."
tokens = tokenizer(text, return_tensors='pt')
with torch.no_grad():
    output = model(**tokens)
 
# Get the sentence vector by averaging token embeddings
sentence_vector = output.last_hidden_state.mean(dim=1)
print(sentence_vector)
```
### [Click Here to see more content about Vectors](Split_content/vectors.md)
---

## Section 6: Knowledge Check: Interview Questions on Vectors

1. What is a vector in the context of Natural Language Processing (NLP)?
2. How are word embeddings different from sentence embeddings?
3. What is the primary purpose of converting text into vectors?
4. What are some common distance metrics used to compare vectors?
5. How does cosine similarity differ from Euclidean distance?
6. How can GPT models (using the `transformers` library) be used to generate vector embeddings?
7. What role does `torch` play in embedding and vector computations?
8. Which library is designed for fast similarity search across large vector databases?
9. What types of mathematical operations can be performed on vectors using `numpy`?
10. Why is vector normalization important in similarity comparison?

---

# 4. Understanding FAISS

## Section 1: 🔍 What is FAISS (Facebook AI Similarity Search)
 
FAISS is a library developed by Facebook AI Research to efficiently search and cluster dense vectors. It is highly optimized and widely used for large-scale similarity search in NLP, computer vision, and recommendation systems.
 
### 📌 Overview
 
**FAISS** stands for **Facebook AI Similarity Search**. It is a powerful library used to perform similarity search on dense vectors with support for **CPU** and **GPU**, optimized for speed and memory efficiency.
 
## Section 2: ✅ When to Use FAISS?
 
- When working with millions of text/document vectors. 
- perform semantic search or recommendation systems. 
- To handle vector similarity tasks at scale. 
- For approximate nearest neighbor (ANN) searches with high performance.
  
## Section 3: ⚙️ Installation
 
### CPU version
pip install faiss-cpu
 
### GPU version
pip install faiss-gpu

---

## Section 4: 🧪 Sample Code

```python
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
 
# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModel.from_pretrained("gpt2")
model.eval()
 
# Generate vector (example for single sentence)
sentence = "Hello world!"
inputs = tokenizer(sentence, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).numpy()
 
# Create FAISS index
index = faiss.IndexFlatL2(embedding.shape[1])
index.add(embedding)
 
# Search
D, I = index.search(embedding, k=1)
print("Distances:", D)
print("Indices:", I)
```
### [Click Here to see more about Faiss](Split_content/Faiss.md) 
---
 
## Section 5: ✅ Knowledge Check : Interview Questions on FAISS
 
1. What is FAISS used for?
2. Which company developed FAISS?
3. What does IndexFlatL2 do?
4. How do you approximate cosine similarity in FAISS? 
5. What is IndexIVFPQ suitable for?
6. Which method normalizes vectors in FAISS?
7. Can FAISS run on GPU?
8. Name two distance metrics supported by FAISS.
9. What is the default distance used in IndexFlatL2?
10. Why is normalization important for cosine similarity?
 
---

# 5.📦 Understanding MongoDB

## Section 1: Overview

MongoDB is a **NoSQL**, document-oriented database designed for scalability, performance, and ease of development. It stores data in flexible, JSON-like documents, making it ideal for modern applications.
 
---
 
## Section 2: 🧩 Key Features
 
| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Document-based**     | Stores data as BSON (Binary JSON) documents                                |
| **Schema-less**        | No rigid schema — each document can have different fields                  |
| **Scalable**           | Supports horizontal scaling with sharding                                  |
| **Indexing**           | Supports single field, compound, text, geospatial indexes                  |
| **Aggregation**        | Powerful aggregation pipeline for data transformation                     |
| **Replication**        | Provides high availability via replica sets                                |
| **ACID Transactions**  | Multi-document ACID transactions (since MongoDB 4.0)                       |
 
---
 
## Section 3: Core Componenets

- **Database**: Container for collections.
- **Collection**: Group of Documents (like Tables in SQL).
- **Document**: BSON (Binary-JSON) format, analogous to a row in RDBMS.

### Example:

```json
{
  "name": "John",
  "email": "john@example.com",
  "skills": ["Python", "MongoDB", "FastAPI"],
  "is_active": true
}
```
---

## Section 4: CRUD Operations 

### 📥 CREATE - Inserting Documents in MongoDB
 
**To insert new data into a MongoDB collection, use:**
 
**➤ `insertOne()`**
- Inserts a **single document** into the collection.
 
```js
db.users.insertOne({
  name: "Surendra",
  age: 22,
  email: "surendra@example.com"
})
```

**➤ `insertMany()`**
- Inserts **multiple documents** into the collection at once.

```js
db.users.insertMany(
  {
    name: "John",
    age: 22,
    email: "John@example.com"
  },
  {
    name: "David",
    age: 25,
    email: "David@example.com"
  }
)
```
---

### 📖 READ - Retrieving Documents from MongoDB
 
**To read or fetch data from a MongoDB collection, we use:**
 
#### 🔹 `find()` - Returns a **cursor** to all matching documents
 
#### ➤ Example: Find all documents
 
```js
db.users.find();
```
#### ➤ Example: Find with Condition

```js
db.users.find({age: { $gt:21 }});
```

#### ➤ Example: Find One Document

```js
db.users.findOne({ name: "John" });
```
---

### UPDATE - Modify Documents

#### ➤ Update One Document

```js
db.users.updateOne(
  { name: "John" },
  { $set: {age: 22 }}
);
```
#### ➤ Update Many Documents

```js
db.users.updateMany(
  { age: { $lt:23 } },
  { $set: { status: "young" } }
);
```
---

### DELETE - Remove Documents

#### ➤ Delete One Document

```js
db.users.deleteOne( { name: "John" } );
```

#### ➤ Delete Many Documents

```js
db.users.deleteMany({age: { $lt: 20} });
```
---

## Section 5: MongoDB Configuration with Python

### Installation

```bash
pip install pymongo
```

```python
from pymongo import MongoClient

# Create connection to local MongoDB server
client = MongoClient("mongodb: //localhost:27017/")

# Access database
db = client["mydatabase"]

# Access collection
collection = db["users"]
```
---

## Section 6: MongoDB Connection with FastAPI

#### Prerequisites

- Python installed
- MongoDB running locally or on Atlas
- Libraries:

```bash
pip install pymongo fastapi uvicorn
```
---

## Section 7: Integrating with FastAPI

```python
from fastapi import FastAPI
from pymongo import MongoClient
 
app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
collection = db["users"]
 
@app.post("/add/")
def add_user(name: str, age: int):
    user = {"name": name, "age": age}
    collection.insert_one(user)
    return {"message": "User added"}
 
@app.get("/users/")
def get_users():
    return list(collection.find({}, {"_id": 0}))
```
**To run the app:**
- uvicorn main:app --reload

---

### [Click Here to see more about MongoDB](Split_Content/mongodb.md)

## Section 8: Knowledge Check: Interview Questions on MongoDB

### 📌 MongoDB Basics
 
1. What is MongoDB and how is it different from RDBMS? 
2. What is a document and a collection? 
3. What is BSON?
4. What port does MongoDB use by default?
5. What is the purpose of _id?
 
### ⚙️ Query Operations
 
6. How do you filter documents using conditions?
7. What are $gt, $lt, $in, $regex?
8. How do you sort, limit, and project fields?
9. What is the difference between update_one() and update_many()?
  
### 🐍 PyMongo
 
10. How do you connect to MongoDB using PyMongo?
11. How do you insert, find, update, and delete documents?
12. How do you work with nested documents? 
13. How do you count or aggregate documents?
 
### 🚀 FastAPI + MongoDB
 
14. What is motor? 
15. How do you create a MongoDB connection with FastAPI? 
16. How to handle _id field (ObjectId) in responses? 
17. How to define Pydantic models for requests?




 
 
 
 
 



 
