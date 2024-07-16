import os
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import string

# Pfad zum Ordner, in dem die CSV-Dateien liegen (relativ zum aktuellen Arbeitsverzeichnis)
folder_path = 'csv'  # Ändere dies entsprechend deinem Ordnerpfad

# Verzeichnis für Diagramme und Textdateien erstellen, wenn es noch nicht existiert
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Liste für alle Daten aus allen CSV-Dateien
data = []

# Durch alle Dateien im Ordner iterieren
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Den vollständigen Pfad zur Datei erstellen
        file_path = os.path.join(folder_path, filename)
        
        # Tabelle aus der CSV-Datei einlesen
        edges_df = pd.read_csv(file_path)
        
        # Überprüfen, ob die notwendigen Spalten vorhanden sind
        if {'From', 'To', 'relation', 'target'}.issubset(edges_df.columns):
            # Daten hinzufügen und '-' Einträge ignorieren
            edges_df.replace('-', '', inplace=True)
            data.extend(edges_df.to_dict('records'))
        else:
            print(f"Fehlende Spalten in Datei: {filename}")

# Variablen für die Ausgabe
construct_some_lines = []
construct_rest_lines = []
where_lines = []
edges = []

# Generator für Variablennamen
variable_names = (f"?{c}" for c in string.ascii_lowercase)

# Durch die gesammelten Daten iterieren
for record in data:
    from_node = record['From']
    to_node = record['To']
    relation = record['relation']
    target = record['target']
    
    # Bedingungen für das Konstruktions- und Abfrageformat hinzufügen
    if from_node and to_node:
        var_from = next(variable_names)
        var_to = next(variable_names)
        construct_some_lines.append(f" {var_to} some {to_node}.")
        where_lines.append(f" {var_from} some {from_node}.")
    if relation and target:
        var_target = next(variable_names)
        construct_rest_lines.append(f" {var_to} {relation} {var_target}.")
        where_lines.append(f" {var_target} some {target}.")
        edges.append((to_node, target, relation))
    elif relation:
        construct_rest_lines.append(f" {var_to} {relation} {var_to}.")
        edges.append((to_node, to_node, relation))

# Textdatei-Inhalt erstellen
construct_text = "CONSTRUCT {  \n" + "\n".join(construct_some_lines) + "\n\n" + "\n".join(construct_rest_lines) + "\n} \n"
where_text = "WHERE {  \n" + "\n".join(where_lines) + "\n} \n"
output_text = construct_text + where_text

# Textdatei speichern
output_file_path = os.path.join(output_dir, 'generated_query.txt')
with open(output_file_path, 'w') as file:
    file.write(output_text)

print(f"Textdatei erfolgreich erstellt und gespeichert unter: {output_file_path}")

# Graph erstellen
G = nx.DiGraph()

# Knoten und Kanten hinzufügen
all_nodes = set()
for edge in edges:
    from_node, to_node, relation = edge
    all_nodes.add(from_node)
    all_nodes.add(to_node)
    G.add_edge(from_node, to_node, label=relation)

# Diagramm erstellen
plt.figure(figsize=(12, 9))

# Verwenden Sie ein Layout, das die Knoten weiter auseinander hält
pos = nx.spring_layout(G, k=2, iterations=50)  # Erhöhen Sie den Wert von k, um die Knoten weiter auseinander zu bringen

# Knoten zeichnen
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')  # Kleinere Knoten

# Kanten zeichnen
nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')

# Kantenbeschriftungen zeichnen
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if 'label' in d}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Knotenbeschriftungen zeichnen
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# Diagramm speichern
plt.title('Automatisiertes Diagramm für alle CSV-Dateien')
plt.savefig(f'{output_dir}/automated_diagram_all.png')
plt.close()

print("Diagramm für alle CSV-Dateien erfolgreich erstellt und gespeichert.")
