import pandas as pd

from evaluation.ragas.evaluation import evaluation


def retrieval_params_evaluation():
    C = {'k':[3,5,10], 'chunk_size': [300, 500, 1000]}
    results = []
    for size in C['chunk_size']:
        for k in C['k']:
            scores = evaluation(k, size)
            results.append({'chunk_size': size, 'k': k, **scores})
    
    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    df.to_csv('retrieval_evaluation_results.csv')

    