---
name: milvus-vector-ops
description: This skill should be used when designing, implementing, debugging, or optimizing Milvus vector database operations — including collection management, hybrid search (dense + sparse), index configuration, embedding insertion, schema design, and performance tuning with pymilvus in async Python services.
metadata:
  category: databases
  source:
    repository: https://github.com/milvus-io/pymilvus
---

# Milvus Vector Database Operations

## Trigger Keywords

`milvus`, `pymilvus`, `vector search`, `vector database`, `dense vector`, `sparse vector`, `BM25`, `hybrid search`, `embedding storage`, `collection`, `ANN search`, `vector index`, `L2 distance`, `cosine similarity`

## Source

- **pymilvus** — GitHub: [milvus-io/pymilvus](https://github.com/milvus-io/pymilvus) (2k+ stars)
- **Milvus** — GitHub: [milvus-io/milvus](https://github.com/milvus-io/milvus) (33k+ stars)
- **Milvus Docs** — https://milvus.io/docs

## Core Principles

### Collection Design
- Use descriptive collection names with project-scoped prefixes: `project_{project_id}`
- Define schema with both dense (float vector) and sparse (sparse float vector) fields for hybrid search
- Always include metadata fields: `document_id`, `chunk_text`, `page_numbers`, `is_image`
- Set appropriate `dim` parameter matching your embedding model output (e.g., 1536 for `text-embedding-3-small`)

### Index Configuration
```python
# Dense vector index (for semantic search)
index_params = {
    "metric_type": "L2",  # or "COSINE" / "IP"
    "index_type": "IVF_FLAT",  # or "HNSW" for better recall
    "params": {"nlist": 128}
}

# Sparse vector index (for BM25 keyword search)
sparse_index_params = {
    "metric_type": "IP",
    "index_type": "SPARSE_INVERTED_INDEX",
    "params": {"drop_ratio_build": 0.2}
}
```

### Hybrid Search Pattern
```python
from pymilvus import AnnSearchRequest, RRFRanker

# Dense search request
dense_req = AnnSearchRequest(
    data=[query_embedding],
    anns_field="dense_vector",
    param={"metric_type": "L2", "params": {"nprobe": 10}},
    limit=top_k
)

# Sparse search request  
sparse_req = AnnSearchRequest(
    data=[sparse_query_vector],
    anns_field="sparse_vector",
    param={"metric_type": "IP"},
    limit=top_k
)

# Combine with Reciprocal Rank Fusion
results = collection.hybrid_search(
    reqs=[dense_req, sparse_req],
    ranker=RRFRanker(k=60),
    limit=top_k,
    output_fields=["chunk_text", "document_id", "page_numbers"]
)
```

### Async Operations
- Use `pymilvus` with async wrappers or run in thread pool for non-blocking operations
- Implement singleton pattern for Milvus connections to reuse across requests
- Always flush after batch inserts to ensure data persistence
- Use `partition_key` for multi-tenant scenarios

### Performance Best Practices
- Batch insert vectors (≤1000 per batch) instead of one-by-one
- Use `load()` before search, `release()` when not needed to manage memory
- Configure `replica_number` for read-heavy workloads
- Monitor via Milvus metrics endpoint (port 9091)
- Use `consistency_level="Bounded"` for better performance when eventual consistency is acceptable

### Error Handling
```python
from pymilvus.exceptions import MilvusException, CollectionNotExistException

try:
    collection.search(...)
except CollectionNotExistException:
    # Create collection first
    create_collection(project_id)
except MilvusException as e:
    logger.error(f"Milvus error: {e.code} - {e.message}")
    raise
```

### Schema Example (Dumatel Pattern)
```python
from pymilvus import CollectionSchema, FieldSchema, DataType

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="document_id", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="chunk_text", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=1536),
    FieldSchema(name="sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
    FieldSchema(name="page_numbers", dtype=DataType.ARRAY, element_type=DataType.INT32, max_capacity=100),
    FieldSchema(name="is_image", dtype=DataType.BOOL),
]
schema = CollectionSchema(fields, description="RAG document chunks")
```

## When NOT to Use
- For relational database queries → use `postgres-pro`
- For Redis caching operations → not applicable
- For general embedding generation → use `rag-architect`
