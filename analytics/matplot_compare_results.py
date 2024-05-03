import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, exc, inspect
import urllib.parse
import os

# Name der Tabelle festlegen
table_name = "RootCalcValues"

# Pandas Dataframe für die Abzufragenden Daten erstellen
df = pd.DataFrame()

# Verbindungszeichenkette für PyODBC erstellen
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=WOODSTOCK\\SQLEXPRESS;"
    "DATABASE=RootCalcValues;"
    "Trusted_Connection=yes;"
)

# Daten abfragen und in Liste speichern
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
            existing_data_query = f"SELECT Radikand, Wurzelexponent, Nachkommastellen, Berechnungszeit_v02, Berechnungszeit_v03, Berechnungszeit_v03_1 FROM {table_name}"
            with engine.connect() as connection:
                existing_data_df = pd.read_sql_query(existing_data_query, connection)
                # Ausgelesene Daten in Liste speichern und Spalten benennen
                existing_data_df.columns = [
                    "Radikand",
                    "Wurzelexponent",
                    "Nachkommastellen",
                    "Berechnungszeit_v02",
                    "Berechnungszeit_v03",
                    "Berechnungszeit_v03_1",
                ]
                df = existing_data_df

except pyodbc.Error as e:
    print(f"Fehler bei der Verbindung oder Abfrage: {e}")
except exc.SQLAlchemyError as e:
    print(f"SQLAlchemy-Fehler: {e}")

# Verbindung sicherheitshalber immer schließen, auch im Falle eines Fehlers
finally:
    conn.close()

print(df.columns)
print(df.head())
# df als csv Datei abspeichern
df.to_csv("existing_data.csv")

# Diagramm erstellen
plt.figure(figsize=(10, 6))
plt.plot(
    df["Nachkommastellen"],
    df["Berechnungszeit_v02"].str.rstrip(" ms").astype(float),
    marker="o",
    label="v02",
)
plt.plot(
    df["Nachkommastellen"],
    df["Berechnungszeit_v03"].str.rstrip(" ms").astype(float),
    marker="o",
    label="v03",
)
plt.plot(
    df["Nachkommastellen"],
    df["Berechnungszeit_v03_1"].str.rstrip(" ms").astype(float),
    marker="o",
    label="v03_1",
)

# Beschriftung
plt.xlabel("Nachkommastellen")
plt.ylabel("Berechnungszeit (ms)")
plt.title("Berechnungszeit vs. Nachkommastellen")

# Legende hinzufügen
plt.legend()

# Diagramm anzeigen
plt.grid()
plt.show()
