# Reranker 
## Overview 
Simple Implementaion of a reranker of chunks retrieved from our vector database.
## Implementation 
- The reranker is based on a cross Encoder model (scores the semantic similarity between two sentences). 
- The model scores the similarity of the query with each retrieved chunk.
- A cross encoder model is slower than searching with KNN on sentence embedding. Then the idea is to retrieve a somewhat large batch of chunks using the vector database and then refine the selection using a smaller k with the reranker.
