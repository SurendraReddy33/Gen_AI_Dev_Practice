## 📐 Distance Metrics (Vector Similarity)
 
To compare vectors, we use distance or similarity metrics:
 
| Metric               | Use Case                          | Range             |
|----------------------|-----------------------------------|-------------------|
| Cosine Similarity     | Semantic similarity               | -1 to 1           |
| Euclidean Distance    | Geometric distance (straight line)| 0 to ∞            |
| Manhattan Distance    | Sum of absolute differences       | 0 to ∞            |
| Dot Product           | Used in attention mechanisms      | -∞ to ∞           |
 
**Note**: Higher cosine similarity means more semantically similar.
 
---

## 🛠️ Common Libraries Used for Vector Operations
 
| Library         | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `numpy`          | A fundamental library for numerical computing in Python. It provides support for arrays, matrices, and vector operations. |
| `scikit-learn`   | A machine learning library that offers tools for clustering, classification, regression, and includes distance metrics (cosine, Euclidean) and normalization methods. |
| `scipy`          | A scientific computing library built on NumPy, used for advanced mathematical functions like spatial distances and linear algebra. |
| `torch`          | A deep learning framework (PyTorch) that supports tensor operations, GPU acceleration, and model training/inference. Used for working with embeddings and neural networks. |
| `transformers`   | Hugging Face library that provides pre-trained models like GPT, BERT, etc., and tools to generate embeddings and perform NLP tasks. |
| `faiss`          | Facebook AI Similarity Search – a library for efficient similarity search and clustering of dense vectors. Used for fast retrieval of similar embeddings. |
---