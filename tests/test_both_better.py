import pandas as pd
import pyodbc
from sqlalchemy import create_engine, exc, inspect
import urllib.parse

import sys
import os

# Verzeichnis des aktuellen Skripts
current_dir = os.path.dirname(__file__)
# Root-Verzeichnis des Projekts
project_rootpath = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_rootpath)
# Import von Modulen relativ zum Root-Verzeichnis
from bin.RootCalc02 import Algebra as Algebra_calc_02
from bin.RootCalc03 import Algebra as Algebra_calc_03
from bin.RootCalc03_1 import Algebra as Algebra_calc_03_1

# Erstellen eines relativen Dateipfades um produzierte Daten in einer Datei zu speichern
# Obsolet da ich einen lokalen SQL-Server benutze
file_path_result_data = os.path.join(current_dir, "../data/better_output_table.csv")

# Funktionen für Übersicht als Variablen definieren
calc_02 = Algebra_calc_02.numeric_root_calc
calc_03 = Algebra_calc_03.numeric_root_calc
calc_03_1 = Algebra_calc_03_1.numeric_root_calc

# Start- und Endparameter für die Schleife die die Daten produziert
rad_start = 1
rad_end = 10

expo_start = 1
expo_end = 10

deci_start = 100
deci_end = 400
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
            # Überprüfe, ob die Werte übereinstimmen
            if result_02 == result_03:
                validation_1 = "Übereinstimmend"
            else:
                validation_1 = "Nicht übereinstimmend"
            if result_03 == result_03:
                validation_2 = "Übereinstimmend"
            else:
                validation_2 = "Nicht übereinstimmend"

            # Formatieren der Zeitangaben
            calc_time_02 = "{:05.0f}".format(time_02 * 1000)
            calc_time_03 = "{:05.0f}".format(time_03 * 1000)
            calc_time_03_1 = "{:05.0f}".format(time_03_1 * 1000)
            # Ergebnisse zur Liste hinzufügen
            export_data.append(
                [
                    radikand,
                    root_exponent,
                    deci_places,
                    calc_time_02,
                    calc_time_03,
                    result_02,
                    validation_1,
                    result_03,
                    calc_time_03_1,
                    result_03_1,
                    validation_2,
                ]
            )

# Daten für den Export in Pandas DataFrame schreiben
columns = [
    "Radikand",
    "Wurzelexponent",
    "Nachkommastellen",
    "Berechnungszeit_v02",
    "Berechnungszeit_v03",
    "v02-Wert",
    "Validation_v02-v03",
    "v03-Wert",
]
# Das nachfolgende ist nur eine kleine Spielerei um zu schauen wie man DataFrames manipulieren kann.
export_data_index1 = [0, 1, 2, 3, 4, 5, 6, 7]
# export_data_df = pd.DataFrame(export_data, columns=columns)
export_data_df = pd.DataFrame(
    [{columns[i]: row[i] for i in export_data_index1} for row in export_data]
)
# Dataframe um weitere Spalte an einer bestimmten Stelle erweitern
insert_index = columns.index("Berechnungszeit_v03")
export_data_df.insert(insert_index + 1, "Berechnungszeit_v03_1", [row[8] for row in export_data])
export_data_df.insert(insert_index + 5, "Validation_v03-v03.1", [row[10] for row in export_data])
# Dataframe um weitere Spalte erweitern
export_data_df["v03.1-Werte"] = [row[9] for row in export_data]

# Ab hier beginnt die Kommunikation mit dem SQL-Server
# Name der Tabelle festlegen
table_name = "RootCalcValues"
# TODO: Automatisches Generieren von Tabellennamen

# Verbindungszeichenkette für PyODBC erstellen
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=WOODSTOCK\\SQLEXPRESS;"
    "DATABASE=RootCalcValues;"
    "Trusted_Connection=yes;"
)

try:
    # PyODBC-Verbindung herstellen
    with pyodbc.connect(connection_string) as conn:
        # SQLAlchemy Engine erstellen
        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
        )

        # Prüfe ob die Tabelle existiert und Frage die vorhandenen Daten ab
        inspector = inspect(engine)
        if inspector.has_table(table_name):
            existing_data_query = (
                f"SELECT Radikand, Wurzelexponent, Nachkommastellen FROM {table_name}"
            )
            with engine.connect() as connection:
                existing_data_df = pd.read_sql_query(existing_data_query, connection)
                # Merge durchführen, um nur die neuen Daten zu behalten
                merged_df = pd.merge(existing_data_df, export_data_df, how="right", indicator=True)
                unique_export_data_df = merged_df[merged_df["_merge"] == "right_only"].drop(
                    "_merge", axis=1
                )
                # Daten in die SQL-Server-Tabelle schreiben
                unique_export_data_df.to_sql(
                    table_name, con=engine, if_exists="append", index=False
                )
        else:
            export_data_df.to_sql(table_name, con=engine, index=False)


except pyodbc.Error as e:
    print(f"Fehler bei der Verbindung oder Abfrage: {e}")

# Verbindung sicherheitshalber immer schließen, auch im Falle eines Fehlers
finally:
    conn.close()
