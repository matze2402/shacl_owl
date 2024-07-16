import os
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

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
construct_lines = []
where_lines = []
edges = []

# Variablen zur Verwendung in den Sparql-Query
variables = ['x', 'y', 'z', 'w', 'v', 'u', 't', 's', 'r', 'q']
var_index = 0

# Durch die gesammelten Daten iterieren
for record in data:
    from_node = record['From']
    to_node = record['To']
    relation = record['relation']
    target = record['target']
    
    # Bedingungen für das Konstruktions- und Abfrageformat hinzufügen
    if from_node and to_node:
        from_var = f"?variable_{variables[var_index]}"
        to_var = f"?variable_{variables[var_index + 1]}"
        construct_lines.append(f" {from_var} some {to_var}.")
        where_lines.append(f" {from_var} some {to_node}.")
        var_index += 2
    if relation and target:
        rel_var = f"?variable_{variables[var_index]}"
        construct_lines.append(f" {from_var} {relation} {rel_var}.")
        where_lines.append(f" {rel_var} some {target}.")
        edges.append((from_node, target, relation))
        var_index += 1
    elif relation:
        rel_var = f"?variable_{variables[var_index]}"
        construct_lines.append(f" {from_var} {relation} {rel_var}.")
        edges.append((from_node, from_node, relation))
        var_index += 1

# Textdatei-Inhalt erstellen
construct_text = "CONSTRUCT {  \n" + "\n".join(construct_lines) + "\n} \n"
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
    all_nodes.add(from_node
