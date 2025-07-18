### 🚀 Key Features
 
- ⚡ Fast nearest-neighbor search (exact & approximate)
- 💻 Works on CPU and GPU
- 🧠 Supports billions of vectors
- 🔍 Multiple index types for different trade-offs
- 📏 Supports different distance metrics (L2, IP, Cosine)
- 🧩 Easy integration with Python/NumPy
 
---

## 🗂️ Index Types
 
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
 
## 📏 Distance Metrics
 
| Metric     | Description                          |
|------------|--------------------------------------|
| `L2`       | Euclidean Distance                   |
| `IP`       | Inner Product (Dot Product)          |
| `Cosine`   | Cosine Similarity (normalized L2/IP) |
 
> ℹ️ For Cosine similarity, normalize vectors before adding/searching.
 
---
 
## 📚 Libraries Commonly Used with FAISS
 
| Library        | Purpose                                           |
|----------------|---------------------------------------------------|
| `faiss`        | Core library for indexing and vector search       |
| `numpy`        | Numerical operations and vector handling          |
| `torch`        | Generate embeddings (e.g., using Transformer models) |
| `transformers` | Convert text to vector embeddings using BERT/GPT |
| `sklearn`      | Optional: clustering, evaluation, preprocessing   |
 
---