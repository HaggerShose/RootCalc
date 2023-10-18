import matplotlib.pyplot as plt
import pandas as pd
import os

# Mit OS Modul relativen Pfad für output_table.csv erstellen
current_script_path = os.path.dirname(__file__)
file_path = os.path.join(current_script_path, "data/output_table.csv")

# Daten aus der CSV-Datei lesen
df = pd.read_csv(file_path)

# Diagramm
plt.figure(figsize=(10, 6))
plt.plot(df["Nachkommastellen"], df["Berechnungszeit"].str.rstrip(" ms").astype(float), marker='o',
         label='devVersion')
plt.plot(df["Nachkommastellen"], df["Berechnungszeit2"].str.rstrip(" ms").astype(float), marker='o',
         label='Legacy')

# Beschriftung
plt.xlabel("Nachkommastellen")
plt.ylabel("Berechnungszeit (ms)")
plt.title("Berechnungszeit vs. Nachkommastellen")

# Legende hinzufügen
plt.legend()

# Diagramm anzeigen
plt.grid()
plt.show()
