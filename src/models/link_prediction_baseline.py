# src/models/link_prediction_baseline.py
"""
Run simple link-prediction baseline on the multimodal graph.

Outputs metrics printed to console.
Usage:
  python link_prediction_baseline.py --graph data/dataset/multimodal_graph.gpickle
"""
import argparse, random
import networkx as nx
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
import numpy as np

def feature_vec(G, u, v):
    cn = len(list(nx.common_neighbors(G, u, v)))
    pa = G.degree(u) * G.degree(v)
    try:
        j = next(nx.jaccard_coefficient(G, [(u,v)]))[2]
    except StopIteration:
        j = 0.0
    return [cn, pa, j]

def run(graph_path, sample_size=500):
    import pickle
    with open(graph_path, "rb") as f:
        G = pickle.load(f)
    users = [n for n,d in G.nodes(data=True) if d.get('type')=='user']
    pos=[]; neg=[]
    # collect positives/negatives among user-user pairs
    for i in range(len(users)):
        for j in range(i+1, len(users)):
            u, v = users[i], users[j]
            if G.has_edge(u,v):
                pos.append((u,v))
            else:
                neg.append((u,v))
    random.shuffle(pos); random.shuffle(neg)
    npos = min(sample_size, len(pos))
    nneg = npos
    pos_s = pos[:npos]; neg_s = neg[:nneg]
    X = [feature_vec(G,u,v) for u,v in (pos_s+neg_s)]
    y = [1]*len(pos_s) + [0]*len(neg_s)
    clf = LogisticRegression(max_iter=1000).fit(X,y)
    probs = clf.predict_proba(X)[:,1]
    print("AUC:", roc_auc_score(y, probs))
    print("AP:", average_precision_score(y, probs))

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--graph", default="data/dataset/multimodal_graph.gpickle")
    p.add_argument("--sample", type=int, default=500)
    args = p.parse_args()
    run(args.graph, args.sample)
