import matplotlib.pyplot as plt
import networkx as nx
import os

# Beispiel-Daten aus der PowerPoint
nodes_a = ['A_1', 'A_2', 'A_3', 'A_4']
nodes_b = ['B_1', 'B_2', 'B_3', 'B_4']
edges = [
   #('A_1', 'B_1', None),
   ('B_1', 'B_2', 'rb_1'),
   ('A_1', 'A_2', 'ra_1'),
   #('A_2', 'B_3', None),
   ('A_2', 'A_3' 'ra_2'),
   ('A_2', 'A_4', 'ra_3'),
   #('A_3', 'B_2', None),
   ('B_2', 'B_3', 'rb_2'),
   ('B_3', 'B_4', 'rb_3'),
   #('A_4', 'B_4', None)
]

# Verzeichnis für Diagramme erstellen
output_dir = 'diagrams'
os.makedirs(output_dir, exist_ok=True)

# Graph erstellen
G = nx.DiGraph()

# Knoten hinzufügen
for node in nodes_a + nodes_b:
   G.add_node(node)

# Kanten hinzufügen
for edge in edges:
   from_node, to_node, relation = edge
   G.add_edge(from_node, to_node, label=relation)

# Diagramm erstellen
pos = nx.spring_layout(G)
plt.figure(figsize=(10, 7))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)})

# Diagramm speichern
plt.title('Automatisiertes Diagramm')
plt.savefig(f'{output_dir}/automated_diagram.png')
plt.close()
