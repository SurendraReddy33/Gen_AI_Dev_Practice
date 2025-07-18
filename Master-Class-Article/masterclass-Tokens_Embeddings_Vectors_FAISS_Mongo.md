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

---

## Section 1: What is a Token?

### Explanation: 
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

## Section 4: Installation

Make sure Python 3.6+ is installed

### Create a Virtual environment
python -m venv gpt_tokens_env

gpt_tokens_env\Scripts\activate.bat

### Install required Libraries
pip install `transformers`

---

## Section 5: Transformers

`Transformers` are cutting-edge deep learning architectures that have transformed the field of Natural Language Processing (NLP). Transformers rely on self-attention mechanisms, allowing them to understand context across entire sequences rather than token-by-token like RNNs. They are used in popular models like GPT, BERT...

## Transformers with GPT Tokenizer

- Provided by Hugging Face under 'transformers' library.
- Pretrained with vocabulary specific to GPT2 or GPT4.
- Converts text -> tokens -> IDs

---

## Section 6: Hugging Face
### 🤗 About Hugging Face
 
**Hugging Face** is a leading open-source AI company that provides a powerful platform for working with **natural language processing (NLP)**, **machine learning**, and **transformers-based models**. It is best known for the `transformers` library, which offers access to **state-of-the-art pre-trained models** like BERT, GPT, RoBERTa, T5, and many more.
 
### 🔧 What Does Hugging Face Offer?
 
- **Transformers Library**  
  A Python library for loading and using pre-trained transformer models for tasks like text classification, tokenization, text generation, translation, and more.
 
- **Tokenizers Library**  
  Fast and efficient tokenizers optimized for NLP pipelines, supporting BPE, WordPiece, SentencePiece, and other algorithms.
 
- **Datasets Library**  
  Curated collection of ready-to-use NLP datasets that integrate easily with training loops.
 
- **Inference API**  
  Cloud-hosted models accessible via simple API calls, enabling inference without heavy compute infrastructure.
 
- **Model Hub**  
  A central repository of 100,000+ pre-trained models contributed by the community and research labs.
 
### 🧠 Why Use Hugging Face?
 
- Simple, unified API for working with a wide variety of models
- Plug-and-play for research and production NLP tasks
- Continuously updated and community-supported
- Compatible with PyTorch, TensorFlow, and JAX

---

## Section 7: GPT Tokenizer Source Code

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

---

## Section 8: Knowledge Check: Interview Questions on Tokens

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
 
## Section 4: 🔍 Examples of Embedding Use Cases
 
- **Semantic Search**: Matching user queries to similar content
- **Intent Recognition**: Understanding user goals in chatbots
- **Question Answering**: Embedding both context and query for retrieval
- **Clustering**: Grouping similar texts together
- **Anomaly Detection**: Comparing embeddings to identify outliers
 
---
 
## Section 5: 🤗 Using Hugging Face for Embeddings (with GPT and Transformers)
 
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

## Section 6: Libraries Used:
 
- transformers: for GPT model and tokenizer
- torch: for handling model input/output tensors

### 🔧 `torch`
 
`torch` is the core library of **PyTorch**, an open-source deep learning framework developed by Facebook's AI Research lab. It is widely used for building and training neural networks and supports dynamic computation graphs.
 
In the context of GPT and embeddings, `torch` is essential for:
 
- Creating and manipulating **tensors** (multi-dimensional arrays).
- Sending data to CPU/GPU for faster computation.
- Feeding input data into models and retrieving output.
- Converting token IDs into embeddings and vice versa.

---

## ❓ Knowledge Check : Interview Questions on Embeddings 
 
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
 
## Section 5: 📐 Distance Metrics (Vector Similarity)
 
To compare vectors, we use distance or similarity metrics:
 
| Metric               | Use Case                          | Range             |
|----------------------|-----------------------------------|-------------------|
| Cosine Similarity     | Semantic similarity               | -1 to 1           |
| Euclidean Distance    | Geometric distance (straight line)| 0 to ∞            |
| Manhattan Distance    | Sum of absolute differences       | 0 to ∞            |
| Dot Product           | Used in attention mechanisms      | -∞ to ∞           |
 
**Note**: Higher cosine similarity means more semantically similar.
 
---
 
## Section 6: 🛠️ Common Libraries Used for Vector Operations
 
| Library         | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `numpy`          | A fundamental library for numerical computing in Python. It provides support for arrays, matrices, and vector operations. |
| `scikit-learn`   | A machine learning library that offers tools for clustering, classification, regression, and includes distance metrics (cosine, Euclidean) and normalization methods. |
| `scipy`          | A scientific computing library built on NumPy, used for advanced mathematical functions like spatial distances and linear algebra. |
| `torch`          | A deep learning framework (PyTorch) that supports tensor operations, GPU acceleration, and model training/inference. Used for working with embeddings and neural networks. |
| `transformers`   | Hugging Face library that provides pre-trained models like GPT, BERT, etc., and tools to generate embeddings and perform NLP tasks. |
| `faiss`          | Facebook AI Similarity Search – a library for efficient similarity search and clustering of dense vectors. Used for fast retrieval of similar embeddings. |
---
 
## Section 7: 🧠 Sample Code: Generate Sentence Vector using GPT
 
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
---

## Section 8: Knowledge Check: Interview Questions on Vectors

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
 
### 🚀 Key Features
 
- ⚡ Fast nearest-neighbor search (exact & approximate)
- 💻 Works on CPU and GPU
- 🧠 Supports billions of vectors
- 🔍 Multiple index types for different trade-offs
- 📏 Supports different distance metrics (L2, IP, Cosine)
- 🧩 Easy integration with Python/NumPy
 
---

## Section 2: ✅ When to Use FAISS?
 
When working with millions of text/document vectors.
 
To perform semantic search or recommendation systems.
 
To handle vector similarity tasks at scale.
 
For approximate nearest neighbor (ANN) searches with high performance.
 
## Section 3: 🗂️ Index Types
 
| Index Type       | Description                                                           |
|------------------|-----------------------------------------------------------------------|
| `IndexFlatL2`    | Brute-force search using Euclidean (L2) distance                     |
| `IndexFlatIP`    | Brute-force search using Inner Product (dot product)                 |
| `IndexIVFFlat`   | Inverted index with flat quantization (efficient on large datasets)  |
| `IndexIVFPQ`     | Inverted index with product quantization (low memory + fast search)  |
| `IndexHNSW`      | Graph-based index (Hierarchical Navigable Small World)               |
| `IndexLSH`       | Locality Sensitive Hashing for binary vectors                        |
| `IndexPQ`        | Product Quantizer index (compresses vectors to save memory)          |
 
---
 
## Section 4: 📏 Distance Metrics
 
| Metric     | Description                          |
|------------|--------------------------------------|
| `L2`       | Euclidean Distance                   |
| `IP`       | Inner Product (Dot Product)          |
| `Cosine`   | Cosine Similarity (normalized L2/IP) |
 
> ℹ️ For Cosine similarity, normalize vectors before adding/searching.
 
---
 
## Section 5: 📚 Libraries Commonly Used with FAISS
 
| Library        | Purpose                                           |
|----------------|---------------------------------------------------|
| `faiss`        | Core library for indexing and vector search       |
| `numpy`        | Numerical operations and vector handling          |
| `torch`        | Generate embeddings (e.g., using Transformer models) |
| `transformers` | Convert text to vector embeddings using BERT/GPT |
| `sklearn`      | Optional: clustering, evaluation, preprocessing   |
 
---
 
## Section 6: ⚙️ Installation
 
### CPU version
pip install faiss-cpu
 
### GPU version
pip install faiss-gpu

---

## Section 7: 🧪 Sample Code

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
 
---
 
## Section 8: ✅ Knowledge Check : Interview Questions on FAISS
 
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

## Section 5: Query Operations
 
**This table summarizes the most commonly used query operations in MongoDB:**
 
| Operator / Method        | Description                                     | Example Usage                                         |
|--------------------------|-------------------------------------------------|--------------------------------------------------------|
| `{ field: value }`       | Match documents where `field` equals `value`   | `{ name: "John" }`                                |
| `$gt`, `$lt`, `$gte`, `$lte` | Comparison (greater/less than)                | `{ age: { $gt: 18 } }`                                |
| `$ne`                    | Not equal to                                    | `{ status: { $ne: "inactive" } }`                     |
| `$in`, `$nin`            | Match values in/not in a list                   | `{ city: { $in: ["Vijayawada", "Hyderabad"] } }`      |
| `$and`                   | Combine multiple conditions (AND)              | `{ $and: [{ age: { $gt: 18 } }, { status: "active" }] }` |
| `$or`                    | Match any condition (OR)                       | `{ $or: [{ age: { $lt: 18 } }, { status: "inactive" }] }` |
| `$not`                   | Negate a condition                             | `{ age: { $not: { $gt: 30 } } }`                      |
| `$exists`                | Check if field exists                          | `{ email: { $exists: true } }`                        |
| `$regex`                 | Pattern matching (like SQL LIKE)               | `{ name: { $regex: "^S" } }`                          |
| `find().limit()`         | Limit number of results                        | `db.users.find().limit(5)`                           |
| `find().sort()`          | Sort results ascending/descending              | `db.users.find().sort({ age: -1 })`                  |
| `find().count()`         | Count number of matching documents             | `db.users.find({ age: { $gt: 20 } }).count()`         |
| `findOne()`              | Fetch a single document                        | `db.users.findOne({ name: "John" })`              |
 
> 📝 Use `db.collection.find(query)` to apply most of the above queries.

---

## Section 6: MongoDB Configuration with Python

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

## Section 7: MongoDB Connection with FastAPI

#### Prerequisites

- Python installed
- MongoDB running locally or on Atlas
- Libraries:

```bash
pip install pymongo fastapi uvicorn
```
---

## Section 8: Integrating with FastAPI

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

## Section 9: Knowledge Check: Interview Questions on MongoDB

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




 
 
 
 
 



 
