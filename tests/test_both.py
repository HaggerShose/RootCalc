import os
import subprocess

import pandas as pd

# Relative Pfade ermitteln und erstellen um die verschiedenen Programme plattformunabhängig auszuführen.
current_path = os.path.dirname(__file__)
file_path_dev = os.path.join(current_path, "../bin/RootCalcdef.py")
file_path_leg = os.path.join(current_path, "../bin/RootCalc02.py")

deci_places = 50
max_deci_places = 1000
data = []

while deci_places <= max_deci_places:

    process = subprocess.Popen(
        ["python", file_path_dev],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        universal_newlines=True)

    # time.sleep(0.1)

    process.stdin.write("2\n")  # Exponent
    process.stdin.write("2\n")  # Radikand
    process.stdin.write(str(deci_places) + "\n")  # Nachkommastellen
    process.stdin.write("exit\n")  # Programm Beenden

    # Eine Variable für den gesamten Output des Programms festlegen
    output, _ = process.communicate()

    """Hier wird der Output gefiltert"""
    # Eine Liste von Trennzeichen
    separators = [":", "?", ". "]

    # Initialisiere die Teile mit der ursprünglichen Zeichenfolge
    parts = [output]

    # Iteriere über die Trennzeichen und teile die Zeichenfolge entsprechend
    for separator in separators:
        new_parts = []
        for part in parts:
            new_parts.extend(part.split(separator))
        parts = new_parts

    # Entfernen von Leerzeichen um die Teile
    parts = [part.strip() for part in parts]
    # Extrahieren und Formatieren der benötigten Werte
    value_berechnungszeit = parts[7].strip(" ms")
    value_berechnungszeit = float(value_berechnungszeit)
    print(f"{deci_places:04d} {value_berechnungszeit:07.3f}ms def")
    # Gefilterte Werte in eine neue Liste eintragen
    data.append(["{:04d}".format(int(deci_places)), "{:07.3f}".format(float(value_berechnungszeit)) + " ms"])
    # Nachkommastellen um 50 erhöhen
    deci_places += 50

# Zweiten Testlauf starten
deci_places = 50  # Zurücksetzen der Nachkommastellen
data2 = []

while deci_places <= max_deci_places:

    process = subprocess.Popen(
        ["python", file_path_leg],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        universal_newlines=True)

    # time.sleep(0.1)

    process.stdin.write("2\n")  # Exponent
    process.stdin.write("2\n")  # Radikand
    process.stdin.write(str(deci_places) + "\n")  # Nachkommastellen
    process.stdin.write("exit\n")  # Programm Beenden

    # Eine Variable für den gesamten Output des Programms festlegen
    output, _ = process.communicate()

    """Hier wird der Output gefiltert"""
    # Eine Liste von Trennzeichen
    separators = [":", "?", ". "]

    # Initialisiere die Teile mit der ursprünglichen Zeichenfolge
    parts = [output]

    for separator in separators:
        new_parts = []
        for part in parts:
            new_parts.extend(part.split(separator))
        parts = new_parts

    # Entfernen von Leerzeichen um die Teile
    parts = [part.strip() for part in parts]
    # Extrahieren und Formatieren der benötigten Werte
    value_berechnungszeit = parts[5].strip(" ms")
    value_berechnungszeit = float(value_berechnungszeit)
    print(f"{deci_places:04d} {value_berechnungszeit:07.3f}ms 02")
    data2.append(["{:04d}".format(int(deci_places)), "{:07.3f}".format(float(value_berechnungszeit)) + " ms"])
    deci_places += 50

# Daten aus dem ersten Programm in PandaDataFrame umwandeln
df1 = pd.DataFrame(data, columns=["Nachkommastellen", "Berechnungszeit"])

# Daten aus dem zweiten Programm in PandaDataFrame umwandeln
df2 = pd.DataFrame(data2, columns=["Nachkommastellen", "Berechnungszeit2"])

# Zusammenführen der beiden DataFrames
result_df = pd.merge(df1, df2, on="Nachkommastellen")

# Daten in eine CSV-Datei schreiben
result_df.to_csv("C:/Users/manue/Desktop/PythonProjekte/Lernprojekte/RootCalc/data/output_table.csv", index=False)
