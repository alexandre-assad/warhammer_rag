# Vector Database 
## Overview 
This module is used to build and search the vector database. It is built on top of ChromaDB.
## Basic Usage 
VectorStore is the main class that abstracts the vector database. 
-   Instantiate the store 
- Populate it (create the database) with index/markdown or add_chunks 
- Query the database using search 
## Implementation details 
For vectorization, we use intfloat/multilingual-e5-small which is lightweight sentence embedding model.
For retrieval, we use HNSW supported by the cosine distance.
We are not implementing a reranker at this time.
The collection is the name of the database that is created.
A source is a markdown file most of the time, where chunks come from
A query can be done with regards to a given source (by specifying the source) or collection wide (all sources)