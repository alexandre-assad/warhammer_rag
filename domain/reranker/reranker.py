from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
class Reranker:
    def __init__(self,model_name=MODEL_NAME):
        self.model = CrossEncoder(model_name)

    def rerank(
            self,
            query: str,
            chunks:list[dict],
            top_k:int =5
    )-> list[dict]: 
        if len(chunks) == 0:
            return []
        scores = self.model.predict([[query,chunk["text"]] for chunk in chunks])
        ranked = sorted(zip(chunks, scores),key = lambda x : x[1],reverse=True)
        return [{**chunk, "rerank_score":float(score)} for chunk, score in ranked[:min(len(chunks),top_k)]]
        