import pandas as pd
import os
import pyodbc
from sqlalchemy import create_engine
import urllib.parse

import sys

from bin.RootCalc02 import Algebra as Algebra_calc_02
from bin.RootCalc03 import Algebra as Algebra_calc_03
from bin.RootCalc03_1 import Algebra as Algebra_calc_03_1

# Erstellen eines relativen Dateipfades um produzierte Daten in einer Datei zu speichern
# Obsolet da ich einen lokalen SQL-Server benutze
current_path = os.path.dirname(__file__)
file_path_result_data = os.path.join(current_path, "../data/better_output_table.csv")

# Funktionen für Übersicht als Variablen definieren
calc_02 = Algebra_calc_02.numeric_root_calc
calc_03 = Algebra_calc_03.numeric_root_calc
calc_03_1 = Algebra_calc_03_1.numeric_root_calc

# Start- und Endparameter für die Schleife die die Daten produziert
rad_start = 1
rad_end = 5
# root_exponent = 2
expo_start = 1
expo_end = 5
# deci_places = 10
deci_start = 500
deci_end = 500
deci_step = 100

# Liste zum Speichern der Daten erstellen
export_data = []

# Schleife zum durchrechnen Verschiedener Werte
for radikand in range(rad_start, rad_end + 1):
    for root_exponent in range(expo_start, expo_end + 1):
        for deci_places in range(deci_start, deci_end + 1, deci_step):
            result_02, time_02 = calc_02(radikand, deci_places, root_exponent)
            result_03, time_03 = calc_03(radikand, deci_places, root_exponent)
            result_03_1, time_03_1 = calc_03_1(radikand, deci_places, root_exponent)
            # Überprüfe, ob die Werte in ergebnis_leg[0] und ergebnis_def[0] übereinstimmen
            if result_02 == result_03:
                validation = "Übereinstimmend"
            else:
                validation = "Nicht übereinstimmend"
            # Formatieren der Zeitangaben
            calc_time_02 = "{:05.0f}".format(time_02 * 100)
            calc_time_03 = "{:05.0f}".format(time_03 * 100)
            calc_time_03_1 = "{:05.0f}".format(time_03_1 * 100)
            # Ergebnisse zur Liste hinzufügen
            export_data.append(
                [
                    radikand,
                    root_exponent,
                    deci_places,
                    validation,
                    calc_time_02,
                    calc_time_03,
                    result_02,
                    result_03,
                    calc_time_03_1,
                    result_03_1,
                ]
            )

# Daten für den Export in Pandas DataFrame schreiben
columns = [
    "Radikand",
    "Wurzelexponent",
    "Nachkommastellen",
    "ErgebnisValidation",
    "Berechnungszeit_v02",
    "Berechnungszeit_v03",
    "v02-Wert",
    "v03-Wert",
]
export_data_index1 = [0, 1, 2, 3, 4, 5, 6, 7]
#export_data_df = pd.DataFrame(export_data, columns=columns)
export_data_df = pd.DataFrame([{columns[i]: row[i] for i in export_data_index1} for row in export_data])

# Dataframe um weitere Spalte erweitern
export_data_df["v03.1-Werte"] = [row[9] for row in export_data]
# Dataframe um weitere Spalte an einer bestimmten Stelle erweitern
insert_index = columns.index("Berechnungszeit_v03")
export_data_df.insert(insert_index + 1, "Berechnungszeit_v03_1", [row[8] for row in export_data])

# Verbindungszeichenkette für PyODBC erstellen
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-9K0O52U\\SQLEXPRESS;"
    "DATABASE=RootCalcValues;"
    "Trusted_Connection=yes;"
)

# PyODBC-Verbindung herstellen
conn = pyodbc.connect(connection_string)

# SQLAlchemy Engine erstellen
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}")

# TODO: Automatisches Generieren von Tabellennamen und Datenabgleich damit keine doppelten Werte gespeichert werden
# Daten in die SQL Server-Tabelle schreiben
export_data_df.to_sql("RootCalcValues2", con=engine, if_exists="replace", index=False)

# Verbindung schließen
conn.close()
