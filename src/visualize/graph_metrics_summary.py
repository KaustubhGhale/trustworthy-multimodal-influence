import networkx as nx
import pickle
from networkx.algorithms import community

# === Load Graph ===
with open("data/dataset/multimodal_graph.gpickle", "rb") as f:
    G = pickle.load(f)

print("\n=== GRAPH METRICS SUMMARY ===")

# --- Basic Stats ---
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
density = nx.density(G)
avg_degree = sum(dict(G.degree()).values()) / num_nodes
avg_clustering = nx.average_clustering(G)

print(f"Total Nodes: {num_nodes}")
print(f"Total Edges: {num_edges}")
print(f"Graph Density: {density:.4f}")
print(f"Average Degree: {avg_degree:.2f}")
print(f"Average Clustering Coefficient: {avg_clustering:.4f}")

# --- Connectivity ---
if nx.is_connected(G):
    diameter = nx.diameter(G)
    print(f"Graph Diameter: {diameter}")
else:
    largest_cc = max(nx.connected_components(G), key=len)
    subG = G.subgraph(largest_cc)
    diameter = nx.diameter(subG)
    print(f"Graph not fully connected — diameter of largest component: {diameter}")

# --- Centrality Metrics ---
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)

# Top influential nodes by degree
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 Influential Nodes (Degree Centrality):")
for node, val in top_degree:
    print(f"  {node}: {val:.4f}")

# --- Community Detection ---
communities = community.greedy_modularity_communities(G)
modularity = community.modularity(G, communities)

print(f"\nDetected Communities: {len(communities)}")
print(f"Modularity Score: {modularity:.4f}")

# --- Summary Conclusion ---
print("\n=== SUMMARY ===")
print("High modularity → distinct communities exist.")
print("High clustering coefficient → localized influence pockets.")
print("Top central nodes represent potential 'key influencers' across modalities.")
print("=============================\n")
