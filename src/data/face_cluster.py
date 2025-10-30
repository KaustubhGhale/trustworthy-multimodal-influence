# src/data/face_cluster.py
"""
Cluster face embeddings to produce person clusters (co-appearance).
Outputs: data/dataset/face_clusters.csv with columns img_id, cluster
Usage:
  python face_cluster.py --emb_dir data/dataset/embeddings --meta data/dataset/metadata.csv
"""
import os, argparse, glob, joblib
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
from tqdm import tqdm

def load_face_embeddings(emb_dir, meta_csv):
    meta = pd.read_csv(meta_csv)
    embs=[]; img_ids=[]
    for _, r in tqdm(meta.iterrows(), total=len(meta)):
        fid = str(r['id'])
        path = os.path.join(emb_dir, f"{fid}_face.pkl")
        if os.path.exists(path):
            try:
                emb = joblib.load(path)
                embs.append(emb)
                img_ids.append(fid)
            except:
                continue
    if len(embs)==0:
        return None, None
    return np.vstack(embs), img_ids

def cluster(emb_dir, meta_csv, out_csv):
    X, img_ids = load_face_embeddings(emb_dir, meta_csv)
    if X is None:
        print("No face embeddings found.")
        return
    model = DBSCAN(eps=0.6, min_samples=1, metric='euclidean').fit(X)
    labels = model.labels_
    df = pd.DataFrame({'img_id': img_ids, 'cluster': labels})
    df.to_csv(out_csv, index=False)
    print("Wrote clusters to", out_csv)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--emb_dir", default="data/dataset/embeddings")
    p.add_argument("--meta", default="data/dataset/metadata.csv")
    p.add_argument("--out", default="data/dataset/face_clusters.csv")
    args = p.parse_args()
    cluster(args.emb_dir, args.meta, args.out)
