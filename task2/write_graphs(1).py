import emoji
import re
import os
import sys
import time
import string
import pickle
import json
import pandas as pd
import csv
import sklearn
import networkx as nx
from networkx.algorithms import bipartite
import network_map2 as nm2

# Read json data:
with open("myfile.json", "r", encoding='utf-8') as json_f:
    sl = json.load(json_f)

data = []
for i in sl:
    for j in sl[i]:
        weight=sl[i][j]
        data.append((i,j, weight))
df = pd.DataFrame(data, columns =['Emoji', 'Word', 'Weight'])

# Sample only 10,000 edges from the original data:
df = sklearn.utils.shuffle(df,random_state = 608)
df_sampled = df.sample(random_state = 608, n = 15000)
# print(df_sampled)
# # Initialize graph G:
G = nx.Graph()
adj_mat = []
for index, row in df_sampled.iterrows():
    adj_mat.append((row[0], row[1], row[2]))
G.add_weighted_edges_from(adj_mat)

# Notice: Need to select the largest connected component of the graph G since G is not entirely connected: 
G_largest = sorted(nx.connected_components(G), key = len, reverse=True)[0]
G_largest = G.subgraph(G_largest)

# # Write the bipartite graph: 
# print("Write the bipartite graph...")
# nx.write_gpickle(G_largest, "./Graphs/bipartite.gpickle")

# Projections:
X, Y = bipartite.sets(G_largest)

rows = sorted(list(Y))

# Simple projections:
print("Generate simple projections and saving...")
Gp_simp = nm2.simple(G_largest, rows)
nx.write_gpickle(Gp_simp, "./Graphs/Gp_simp_10k.gpickle")

# Hyperbolic projection:
print("Generate Hyperbolic projection and saving...")
Gp_hyper = nm2.hyperbolic(G_largest, rows)
nx.write_gpickle(Gp_hyper, "./Graphs/Gp_hyper_10k.gpickle")

# YCN random walks:
print("Generate YCN random walks and saving...")
Gp_ycn = nm2.ycn(G_largest, rows, directed = True)
nx.write_gpickle(Gp_ycn, "./Graphs/Gp_ycn_10k.gpickle")

# ProbS:
print("Generate ProbS and saving...")
Gp_probs = nm2.probs(G_largest, rows, directed = True)
nx.write_gpickle(Gp_probs, "./Graphs/Gp_probs_10k.gpickle")

# HeatS:
print("Generate HeatS and saving...")
Gp_heats = nm2.heats(G_largest, rows, directed = True)
nx.write_gpickle(Gp_heats, "./Graphs/Gp_heats_10k.gpickle")

# Hybrid:
print("Generate Hybrid with 0.5 weights and saving...")
Gp_hybrid = nm2.hybrid(G_largest, rows, .5, directed = True)
nx.write_gpickle(Gp_hybrid, "./Graphs/Gp_hybrid_10k.gpickle")