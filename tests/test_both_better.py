import pandas as pd
import os
import pyodbc
from sqlalchemy import create_engine
import urllib.parse

import sys

from bin.RootCalc02 import Algebra as Algebra_calc_02
from bin.RootCalc03 import Algebra as Algebra_calc_03

current_path = os.path.dirname(__file__)
file_path_result_data = os.path.join(current_path, "../data/better_output_table.csv")

calc_02 = Algebra_calc_02.numeric_root_calc
calc_03 = Algebra_calc_03.numeric_root_calc

rad_start = 1
rad_end = 101
root_exponent = 2
deci_places = 10

# Liste zum Speichern der Ergebnisse erstellen
export_data = []

# Schleife zum durchrechnen Verschiedener Werte
for radikand in range(rad_start, rad_end):
    ergebnis_02 = calc_02(radikand, deci_places, root_exponent)
    ergebnis_03 = calc_03(radikand, deci_places, root_exponent)
    # Überprüfe, ob die Werte in ergebnis_leg[0] und ergebnis_def[0] übereinstimmen
    if ergebnis_02[0] == ergebnis_03[0]:
        validation = "Übereinstimmend"
    else:
        validation = "Nicht übereinstimmend"
    # Formatieren der Zeitangaben
    calc_time_02 = "{:05.0f}".format(ergebnis_02[1] * 100)
    calc_time_03 = "{:05.0f}".format(ergebnis_03[1] * 100)
    # Ergebnisse zur Liste hinzufügen
    export_data.append(
        [
            radikand,
            root_exponent,
            deci_places,
            validation,
            calc_time_02,
            calc_time_03,
            ergebnis_02[0],
            ergebnis_03[0],
        ]
    )

# Daten für den Export in Pandas DataFrame umwandeln
columns = [
    "Radikand",
    "Wurzelexponent",
    "Nachkommastellen",
    "ErgebnisValidation",
    "Berechnungszeit_Leg",
    "Berechnungszeit_Def",
    "Leg-Wert",
    "Dev-Wert",
]
export_data_df = pd.DataFrame(export_data, columns=columns)

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

# Daten in die SQL Server-Tabelle schreiben
export_data_df.to_sql("RootCalcValues", con=engine, if_exists="replace", index=False)

# Verbindung schließen
conn.close()
