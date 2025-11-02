# src/models/train_gnn_lite.py
"""
Lightweight link predictor (MLP) on sampled user-user pairs.
Usage:
  python train_gnn_lite.py --graph data/dataset/multimodal_graph.gpickle --emb_dir data/dataset/embeddings
"""
import argparse, networkx as nx, numpy as np, torch, torch.nn as nn, torch.optim as optim
from sklearn.metrics import roc_auc_score, average_precision_score
import random, joblib

class LinkMLP(nn.Module):
    def __init__(self, in_dim=10, hid=32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(in_dim*2, hid), nn.ReLU(), nn.Linear(hid,1), nn.Sigmoid())
    def forward(self, a, b):
        x = torch.cat([a,b], dim=1)
        return self.net(x).squeeze()

def load_node_features(G, emb_dir):
    users = [n for n,d in G.nodes(data=True) if d.get('type')=='user']
    idx = {u:i for i,u in enumerate(users)}
    X = []
    for u in users:
        deg = G.degree(u)
        # average visual embeddings of user's images if present
        vis_feats=[]
        for nb in G[u]:
            if G.nodes[nb].get('type')=='image':
                file_tag = G.nodes[nb].get('file')
                if file_tag:
                    # filename id extraction
                    # embeddings saved as <id>_vis.pkl
                    fname = file_tag
                    base = None
                    try:
                        base = int(str(os.path.basename(fname)).split('.')[0])
                    except:
                        pass
                # try to load vis embedding by id if exists
        # For Lite we only use degree + random small vector
        vec = np.concatenate(([deg], np.random.normal(size=9)))
        X.append(vec.astype('float32'))
    return np.array(X), users, idx

import os
def run(graph_path, emb_dir, epochs=200):
    import pickle
    with open(graph_path, "rb") as f:
        G = pickle.load(f)

    X, users, idx = load_node_features(G, emb_dir)
    N = X.shape[0]
    # prepare pairs
    pos=[]; neg=[]
    for i in range(N):
        for j in range(i+1,N):
            if G.has_edge(users[i], users[j]):
                pos.append((i,j,1))
            else:
                neg.append((i,j,0))
    random.shuffle(pos); random.shuffle(neg)
    npos = min(500, len(pos))
    pairs = pos[:npos] + neg[:npos]
    random.shuffle(pairs)
    a_idx = torch.tensor([p[0] for p in pairs], dtype=torch.long)
    b_idx = torch.tensor([p[1] for p in pairs], dtype=torch.long)
    y = torch.tensor([p[2] for p in pairs], dtype=torch.float32)
    X_t = torch.tensor(X, dtype=torch.float32)
    model = LinkMLP(in_dim=X.shape[1])
    opt = optim.Adam(model.parameters(), lr=1e-3)
    for epoch in range(epochs):
        model.train()
        opt.zero_grad()
        preds = model(X_t[a_idx], X_t[b_idx])
        loss = nn.BCELoss()(preds, y)
        loss.backward(); opt.step()
        if epoch%50==0:
            with torch.no_grad():
                auc = roc_auc_score(y.numpy(), preds.detach().numpy())
                print(f"Epoch {epoch} loss {loss.item():.4f} auc {auc:.4f}")
    with torch.no_grad():
        preds = model(X_t[a_idx], X_t[b_idx]).numpy()
        print("Final AUC:", roc_auc_score(y.numpy(), preds))
        print("Final AP:", average_precision_score(y.numpy(), preds))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--graph", default="data/dataset/multimodal_graph.gpickle")
    p.add_argument("--emb_dir", default="data/dataset/embeddings")
    p.add_argument("--epochs", type=int, default=200)
    args = p.parse_args()
    run(args.graph, args.emb_dir, args.epochs)
