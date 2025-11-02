import networkx as nx
import pickle
import matplotlib.pyplot as plt
from networkx.algorithms import community

# === Load Graph ===
with open("data/dataset/multimodal_graph.gpickle", "rb") as f:
    G = pickle.load(f)

# === Compute Communities using the Greedy Modularity Algorithm ===
communities = community.greedy_modularity_communities(G)
print(f"Detected {len(communities)} communities.")

# Assign community ID to each node
community_map = {}
for i, comm in enumerate(communities):
    for node in comm:
        community_map[node] = i

# === Compute Influence (Degree Centrality) ===
centrality = nx.degree_centrality(G)
top_influencers = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]

print("\nTop 10 Influential Nodes:")
for node, score in top_influencers:
    print(f"{node}: {score:.4f}")

# === Visualization ===
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, seed=42)

# Draw nodes with community colors and size proportional to influence
node_colors = [community_map.get(n, 0) for n in G.nodes()]
node_sizes = [centrality[n] * 6000 for n in G.nodes()]

nx.draw_networkx_nodes(
    G,
    pos,
    node_color=node_colors,
    node_size=node_sizes,
    cmap=plt.cm.tab20,
    alpha=0.8,
)

nx.draw_networkx_edges(G, pos, alpha=0.2)
nx.draw_networkx_labels(
    G,
    pos,
    labels={n: n for n, _ in top_influencers},
    font_size=8,
    font_color="black",
)

plt.title("Community + Influence Visualization of the Multimodal Graph", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
