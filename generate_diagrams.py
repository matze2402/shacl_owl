import os
import pandas as pd

# Pfad zum Ordner, in dem die CSV-Dateien liegen (relativ zum aktuellen Arbeitsverzeichnis)
folder_path = 'csv'  # Ändere dies entsprechend deinem Ordnerpfad

# Verzeichnis für Textdateien erstellen, wenn es noch nicht existiert
output_dir = 'text_files'
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

# Durch die gesammelten Daten iterieren
for record in data:
    from_node = record['From']
    to_node = record['To']
    relation = record['relation']
    target = record['target']
    
    # Bedingungen für das Konstruktions- und Abfrageformat hinzufügen
    if from_node and to_node:
        construct_lines.append(f" ?variable_{to_node.lower()}  some  {to_node}.")
        where_lines.append(f" ?variable_{from_node.lower()}  some  {from_node}.")
    if relation and target:
        construct_lines.append(f" ?variable_{to_node.lower()}  {relation}  ?variable_{target.lower()}.")
        where_lines.append(f" ?variable_{target.lower()}  some  {target}.")
    elif relation:
        construct_lines.append(f" ?variable_{to_node.lower()}  {relation}  ?variable_{to_node.lower()}.")

# Textdatei-Inhalt erstellen
construct_text = "CONSTRUCT {  \n" + "\n".join(construct_lines) + "\n} \n"
where_text = "WHERE {  \n" + "\n".join(where_lines) + "\n} \n"
output_text = construct_text + where_text

# Textdatei speichern
output_file_path = os.path.join(output_dir, 'generated_query.txt')
with open(output_file_path, 'w') as file:
    file.write(output_text)

print(f"Textdatei erfolgreich erstellt und gespeichert unter: {output_file_path}")
