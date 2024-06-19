import os
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Pfad zum Ordner, in dem die CSV-Dateien liegen (relativ zum aktuellen Arbeitsverzeichnis)
folder_path = 'csv'  # Ändere dies entsprechend deinem Ordnerpfad

# Verzeichnis für Diagramme erstellen, wenn es noch nicht existiert
output_dir = 'diagrams'
os.makedirs(output_dir, exist_ok=True)

# Liste für alle Kanten aus allen CSV-Dateien
edges = []

# Durch alle Dateien im Ordner iterieren
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Den vollständigen Pfad zur Datei erstellen
        file_path = os.path.join(folder_path, filename)
        
        # Tabelle aus der CSV-Datei einlesen
        edges_df = pd.read_csv(file_path)
        
        # Überprüfen, ob die notwendigen Spalten vorhanden sind
        if {'from_node', 'to_node', 'relation', 'target'}.issubset(edges_df.columns):
            # Zu Kanten (from_node, to_node, relation, target) konvertieren und zur Liste hinzufügen
            edges.extend(list(zip(edges_df['from_node'], edges_df['to_node'], edges_df['relation'], edges_df['target'])))
        else:
            print(f"Fehlende Spalten in Datei: {filename}")

# Graph erstellen
G = nx.DiGraph()

# Alle Knoten hinzufügen
all_nodes = set()
for edge in edges:
    all_nodes.add(edge[0])
    all_nodes.add(edge[1])
    all_nodes.add(edge[3])  # Target auch als Knoten hinzufügen

for node in all_nodes:
    G.add_node(node)

# Kanten hinzufügen
for edge in edges:
    from_node, to_node, relation, target = edge
    G.add_edge(from_node, to_node, label=relation)
    G.add_edge(to_node, target, label=f"target ({relation})")  # Verbindung zwischen to_node und target

# Diagramm erstellen
pos = nx.spring_layout(G)
plt.figure(figsize=(12, 9))

# Knoten zeichnen
nx.draw_networkx_nodes(G, pos, node_size=100, node_color='lightblue')

# Kanten zeichnen
nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')

# Kantenbeschriftungen zeichnen
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)})

# Knotenbeschriftungen zeichnen
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# Diagramm speichern
plt.title('Automatisiertes Diagramm für alle CSV-Dateien')
plt.savefig(f'{output_dir}/automated_diagram_all.png')
plt.close()

print("Diagramm für alle CSV-Dateien erfolgreich erstellt und gespeichert.")
