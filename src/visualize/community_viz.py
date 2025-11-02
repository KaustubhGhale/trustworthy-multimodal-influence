import networkx as nx
import pickle
import matplotlib.pyplot as plt


with open("data/dataset/multimodal_graph.gpickle", "rb") as f:
    G = pickle.load(f)
communities = nx.algorithms.community.greedy_modularity_communities(G)

plt.figure(figsize=(10,10))
pos = nx.spring_layout(G, k=0.15)
nx.draw_networkx_nodes(G, pos, node_size=50, node_color='skyblue')
nx.draw_networkx_edges(G, pos, alpha=0.2)
plt.title("Detected Communities in Multimodal Social Graph")
plt.show()