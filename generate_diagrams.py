import matplotlib.pyplot as plt
import os

# Beispiel-Daten
data = {
    'A_1': [1, 2, 3],
    'A_2': [4, 5, 6],
    'A_3': [7, 8, 9],
    'A_4': [10, 11, 12]
}

# Verzeichnis für Diagramme erstellen
output_dir = 'diagrams'
os.makedirs(output_dir, exist_ok=True)

# Diagramme erstellen
for key, values in data.items():
    plt.figure()
    plt.plot(values)
    plt.title(f'Diagramm für {key}')
    plt.savefig(f'{output_dir}/{key}.png')
    plt.close()
