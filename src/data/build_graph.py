# src/data/build_graph.py
"""
Build multimodal graph from metadata + cv outputs.

Outputs:
  data/dataset/multimodal_graph.gpickle
Usage:
  python build_graph.py --meta data/dataset/metadata.csv --cv data/dataset/cv_metadata_lite.csv --faces data/dataset/face_clusters.csv
"""
import argparse, os
import pandas as pd
import networkx as nx

def build(meta_csv, cv_csv, faces_csv, out_path):
    meta = pd.read_csv(meta_csv)
    cv = pd.read_csv(cv_csv) if os.path.exists(cv_csv) else pd.DataFrame()
    G = nx.Graph()

    # if metadata has owner column, anonymize, else create pseudo-user per image
    if 'owner' in meta.columns:
        meta['user_anon'] = meta['owner'].apply(lambda x: f"user_{abs(hash(str(x)))%1000000}")
    else:
        meta['user_anon'] = meta['id'].apply(lambda x: f"user_{x}")

    # add user + image nodes
    for _, r in meta.iterrows():
        uid = r['user_anon']
        iname = f"img_{r['id']}"
        G.add_node(uid, type='user')
        G.add_node(iname, type='image', file=r.get('file'), title=r.get('title'))
        G.add_edge(uid, iname, type='posted')

    # add person clusters + contains edges
    if os.path.exists(faces_csv):
        faces = pd.read_csv(faces_csv)
        for _, fr in faces.iterrows():
            cid = int(fr['cluster'])
            person_node = f"person_{cid}"
            G.add_node(person_node, type='person_cluster')
            img_node = f"img_{fr['img_id']}"
            if G.has_node(img_node):
                G.add_edge(img_node, person_node, type='contains')

        # coappearance -> user-user edges
        grouped = faces.groupby('cluster')['img_id'].apply(list).to_dict()
        for cluster, imgs in grouped.items():
            users=set()
            for iid in imgs:
                rows = meta[meta['id']==int(iid)]
                if len(rows)>0:
                    users.add(rows.iloc[0]['user_anon'])
            users = list(users)
            for i in range(len(users)):
                for j in range(i+1, len(users)):
                    if G.has_edge(users[i], users[j]):
                        G[users[i]][users[j]]['weight'] = G[users[i]][users[j]].get('weight',0)+1
                    else:
                        G.add_edge(users[i], users[j], weight=1, type='coappearance')

    import pickle
    with open(out_path, "wb") as f:
        pickle.dump(G, f)
    print("Saved graph to", out_path, "with", G.number_of_nodes(), "nodes and", G.number_of_edges(), "edges")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--meta", default="data/dataset/metadata.csv")
    p.add_argument("--cv", default="data/dataset/cv_metadata_lite.csv")
    p.add_argument("--faces", default="data/dataset/face_clusters.csv")
    p.add_argument("--out", default="data/dataset/multimodal_graph.gpickle")
    args = p.parse_args()
    build(args.meta, args.cv, args.faces, args.out)
