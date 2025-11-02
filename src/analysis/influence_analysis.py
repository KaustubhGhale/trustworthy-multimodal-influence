import networkx as nx
import pickle
import matplotlib.pyplot as plt

# Load your final multimodal graph safely using pickle
with open("data/dataset/multimodal_graph.gpickle", "rb") as f:
    G = pickle.load(f)

# Compute degree centrality as a measure of influence
centrality = nx.degree_centrality(G)

# Sort and display top 10 influential nodes
top_influencers = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]

print("\nTop Influencers in the Multimodal Graph:")
for node, score in top_influencers:
    print(f"{node}: {score:.4f}")

# Optionally visualize
plt.figure(figsize=(10, 8))
nx.draw_networkx(
    G,
    with_labels=False,
    node_size=[v * 5000 for v in centrality.values()],
    alpha=0.6,
    node_color=list(centrality.values()),
    cmap=plt.cm.plasma,
)
plt.title("Influence Visualization by Node Degree")
plt.axis("off")
plt.show()
