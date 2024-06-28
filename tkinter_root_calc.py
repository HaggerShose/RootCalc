import decimal as dci
import tkinter as tk
from tkinter import ttk

from bin import RootCalc02, RootCalc03, RootCalc03_1, RootCalc04


# Funktion um das Ergebnis von Version 2 ins Ausgabefenster zu schreiben
def calc_method_02():
    result, calc_time = RootCalc02.Algebra.numeric_root_calc(
        radikand=dci.Decimal(radikand.get()),
        deci_places=int(deci_places.get()),
        root_exponent=dci.Decimal(exponent.get()),
    )
    # Ergebnis in Ausgabefenster schreiben
    result_frame.config(state="normal")
    result_frame.delete("1.0", "end")
    result_frame.insert("1.0", result)
    result_frame.config(state="disabled")
    # Berechnungszeit formatieren und in Berechnungszeitfenster schreiben
    calc_timef = "{:05.0f}".format(calc_time * 1000) + " ms"
    calc_time_frame.config(state="normal")
    calc_time_frame.delete("1.0", "end")
    calc_time_frame.insert("1.0", calc_timef)
    calc_time_frame.config(state="disabled")


# Funktion um das Ergebnis von Version 3 ins Ausgabefenster zu schreiben
def calc_method_03():
    result, calc_time = RootCalc03.Algebra.numeric_root_calc(
        radikand=dci.Decimal(radikand.get()),
        deci_places=int(deci_places.get()),
        root_exponent=dci.Decimal(exponent.get()),
    )
    # Ergebnis in Ausgabefenster schreiben
    result_frame.config(state="normal")
    result_frame.delete("1.0", "end")
    result_frame.insert("1.0", result)
    result_frame.config(state="disabled")
    # Berechnungszeit formatieren und in Berechnungszeitfenster schreiben
    calc_timef = "{:05.0f}".format(calc_time * 1000) + " ms"
    calc_time_frame.config(state="normal")
    calc_time_frame.delete("1.0", "end")
    calc_time_frame.insert("1.0", calc_timef)
    calc_time_frame.config(state="disabled")


# Funktion um das Ergebnis von Version 3.1 ins Ausgabefenster zu schreiben
def calc_method_03_1():
    result, calc_time = RootCalc03_1.Algebra.numeric_root_calc(
        radikand=dci.Decimal(radikand.get()),
        deci_places=int(deci_places.get()),
        root_exponent=dci.Decimal(exponent.get()),
    )

    # Ergebnis in Ausgabefenster schreiben
    result_frame.config(state="normal")
    result_frame.delete("1.0", "end")
    result_frame.insert("1.0", result)
    result_frame.config(state="disabled")
    # Berechnungszeit formatieren und in Berechnungszeitfenster schreiben
    calc_timef = "{:05.0f}".format(calc_time * 1000) + " ms"
    calc_time_frame.config(state="normal")
    calc_time_frame.delete("1.0", "end")
    calc_time_frame.insert("1.0", calc_timef)
    calc_time_frame.config(state="disabled")


# Funktion um das Ergebnis von Version 4 ins Ausgabefenster zu schreiben
def calc_method_04():
    result, calc_time = RootCalc04.Algebra.numeric_root_calc(
        radikand=dci.Decimal(radikand.get()),
        deci_places=int(deci_places.get()),
        root_exponent=dci.Decimal(exponent.get()),
    )

    # Ergebnis in Ausgabefenster schreiben
    result_frame.config(state="normal")
    result_frame.delete("1.0", "end")
    result_frame.insert("1.0", result)
    result_frame.config(state="disabled")
    # Berechnungszeit in Berechnungszeitfenster schreiben
    # Werte werden ab ver4 schon vorformatiert weiter gegeben
    calc_time_frame.config(state="normal")
    calc_time_frame.delete("1.0", "end")
    calc_time_frame.insert("1.0", calc_time)
    calc_time_frame.config(state="disabled")


# Funktion um die Berechnungsmethode über das DropDown Menu einzustellen
def change_calc_method(event):
    selected_method = calc_method.get()
    if selected_method == "Version 2":
        calc_button.config(command=calc_method_02)
    if selected_method == "Version 3":
        calc_button.config(command=calc_method_03)
    if selected_method == "Version 3.1":
        calc_button.config(command=calc_method_03_1)
    if selected_method == "Version 4":
        calc_button.config(command=calc_method_04)


# Funktion um die Eingeben zu prüfen damit Exceptions vermieden werden
def validate_input(action, value_if_allowed):
    if action == "1":  # Eingabeaktion
        if value_if_allowed.isdigit() or value_if_allowed in (
            "",
            "-",
        ):  # Nur Ziffern, leere Eingabe oder einzelnes Minuszeichen
            return True
        elif value_if_allowed.startswith("-") and value_if_allowed[1:].isdigit():  # Negative Zahlen
            return True
        else:
            mainframe.bell()  # spielt einen nervigen Ton ab, wenn man keine Zahl eingibt
            return False
    return True


# RootFrame
root = tk.Tk()
root.title("Wurzelrechner")
root.resizable(True, True)

# MainFrame in dem alle Widgets angeordnet werden
mainframe = ttk.Frame(root, padding="5 5 10 10")
mainframe.grid(column=0, row=0, sticky="NSEW")

# Verhalten beim Vergrößern des Fensters steuern
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=0)
mainframe.columnconfigure(2, weight=0)
mainframe.columnconfigure(3, weight=0)
mainframe.columnconfigure(4, weight=0)

mainframe.rowconfigure(1, weight=1)


# DropdownMenu um die Berechnungsmethode zu wechseln
calc_method = tk.StringVar()
calc_method_box = ttk.Combobox(
    mainframe, textvariable=calc_method, values=["Version 3.1", "Version 3", "Version 2"]
)
calc_method_box.bind("<<ComboboxSelected>>", change_calc_method)
calc_method_box.state(["readonly"])
calc_method.set("Version 4")
calc_method_box.grid(column=1, row=0, sticky="W")

# Beschriftung für DropDownMenü erstellen und ausrichten
calc_method_label = tk.Label(mainframe, text="Berechnungsmethode:")
calc_method_label.grid(column=0, row=0, sticky="E")


# Ausgabefenster erstellen
result_frame = tk.Text(mainframe, height=5, state="disabled")
result_frame.grid(column=0, row=1, columnspan=5, sticky="NSEW", padx=(5, 0), pady=5)

# Scrollbar erstellen und mit Ausgabefenster verknüpfen
result_frame_scrollbar = ttk.Scrollbar(mainframe, command=result_frame.yview)
result_frame["yscrollcommand"] = result_frame_scrollbar.set
result_frame_scrollbar.grid(column=5, row=1, sticky="NSW")


# Berechnungszeit-Fenster erstellen
calc_time_frame = tk.Text(mainframe, height=1, width=8, state="disabled")
calc_time_frame.grid(column=4, row=2, sticky="W", padx=(5, 0), pady=5)

# Beschriftung für Berechnungszeitfenster
calc_time_label = tk.Label(mainframe, text="Berechnungszeit:")
calc_time_label.grid(column=3, row=2, sticky="W")


# Validate Input Funktion registrieren
validate_input_command = root.register(validate_input)


# Eingabefeld für den Wurzelexponenten
exponent = tk.StringVar()
expo_entry = ttk.Entry(
    mainframe,
    width=15,
    textvariable=exponent,
    validate="key",
    validatecommand=(validate_input_command, "%d", "%P"),
)
expo_entry.grid(column=2, row=3, sticky="E")

# Beschriftung für Wurzelexponenten Eingabefeld erstellen und ausrichten
expo_label = tk.Label(mainframe, text="Exponent:")
expo_label.grid(column=1, row=3, sticky="E")


# Eingabefeld für den zu berechnenden Radikand
radikand = tk.StringVar()
radikand_entry = ttk.Entry(
    mainframe,
    width=15,
    textvariable=radikand,
    validate="key",
    validatecommand=(validate_input_command, "%d", "%P"),
)
radikand_entry.grid(column=2, row=4, sticky="E")

# Beschriftung für Radikand Eingabefeld erstellen und ausrichten
radi_label = tk.Label(mainframe, text="Radikand:")
radi_label.grid(column=1, row=4, sticky="E")


# Eingabefeld für die Anzahl der Nachkommastellen
deci_places = tk.StringVar()
deci_places_entry = ttk.Entry(
    mainframe,
    width=15,
    textvariable=deci_places,
    validate="key",
    validatecommand=(validate_input_command, "%d", "%P"),
)
deci_places_entry.grid(column=2, row=5, sticky="E")

# Beschriftung für Nachkommastellen Eingabefeld erstellen und ausrichten
deci_label = tk.Label(mainframe, text="Nachkommastellen:")
deci_label.grid(column=1, row=5, sticky="E")


# Button für die Berechnung
calc_button = ttk.Button(mainframe, text="Berechnen!", command=calc_method_04)
calc_button.grid(column=3, row=5, sticky="W")


# Allgemeine Einstellungen
for child in mainframe.winfo_children():
    if child not in [result_frame_scrollbar, result_frame]:
        child.grid_configure(padx=5, pady=5)
expo_entry.focus()
root.bind("<Return>", lambda event: calc_button.invoke())

# Mindestgröße des Fensters festlegen
root.update_idletasks()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()

# TODO: Negative Eingaben richtig weitergeben und Methoden dafür aktualisieren
