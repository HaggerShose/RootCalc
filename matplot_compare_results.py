import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, exc, inspect
import urllib.parse
import os


# Name der Tabelle festlegen
table_name = "RootCalcValues2"

# Verbindungszeichenkette für PyODBC erstellen
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-9K0O52U\\SQLEXPRESS;"
    "DATABASE=RootCalcValues;"
    "Trusted_Connection=yes;"
)

try:
    # PyODBC-Verbindung herstellen
    with pyodbc.connect(connection_string) as conn:
        # SQLAlchemy Engine erstellen
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}")
        # Prüfe ob die Tabelle existiert und Frage die vorhandenen Daten ab
        inspector = inspect(engine)
        if inspector.has_table(table_name):
            existing_data_query = f"SELECT Radikand, Wurzelexponent, Nachkommastellen, Berechnungszeit_v02, Berechnungszeit_v03, Berechnungszeit_v03_1 FROM {table_name}"
            with engine.connect() as connection:
                existing_data_df = pd.read_sql_query(existing_data_query, connection)
except pyodbc.Error as e:
    print(f"Fehler bei der Verbindung oder Abfrage: {e}")

# Verbindung sicherheitshalber immer schließen, auch im Falle eines Fehlers
finally:
    conn.close()

# TODO: Graph erstellen lassen

# Daten aus der CSV-Datei lesen
df = pd.read_csv(file_path)

# Diagramm
plt.figure(figsize=(10, 6))
plt.plot(df["Nachkommastellen"], df["Berechnungszeit"].str.rstrip(" ms").astype(float), marker="o", label="devVersion")
plt.plot(df["Nachkommastellen"], df["Berechnungszeit2"].str.rstrip(" ms").astype(float), marker="o", label="Legacy")

# Beschriftung
plt.xlabel("Nachkommastellen")
plt.ylabel("Berechnungszeit (ms)")
plt.title("Berechnungszeit vs. Nachkommastellen")

# Legende hinzufügen
plt.legend()

# Diagramm anzeigen
plt.grid()
plt.show()
