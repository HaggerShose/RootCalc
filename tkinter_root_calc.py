import decimal as dci
import tkinter as tk
from tkinter import ttk

from bin import RootCalcdef, RootCalc02


# Funktion um das Ergebnis Dev Methode ins Ausgabefenster zu schreiben
def calculate_dev():
    result = RootCalcdef.Algebra.numeric_root_calc(radikand=dci.Decimal(radikand.get()),
                                                   deci_places=int(
                                                       deci_places.get()),
                                                   root_exponent=dci.Decimal(exponent.get()))
    result_frame.config(state="normal")
    result_frame.delete("1.0", "end")
    result_frame.insert("1.0", result[0])
    result_frame.config(state="disabled")


# Funktion um das Ergebnis der Legacy Methode ins Ausgabefenster zu schreiben
def calculate_legacy():
    result = RootCalc02.Algebra.numeric_root_calc(radikand=dci.Decimal(radikand.get()),
                                                  deci_places=int(
                                                      deci_places.get()),
                                                  root_exponent=dci.Decimal(exponent.get()))
    result_frame.config(state="normal")
    result_frame.delete("1.0", "end")
    result_frame.insert("1.0", result[0])
    result_frame.config(state="disabled")


# Funktion um die Berechnungsmethode über das DropDown Menu einzustellen
def change_calc_method(event):
    selected_method = calc_method.get()
    if selected_method == "DevVersion":
        calc_button.config(command=calculate_dev)
    elif selected_method == "Legacy":
        calc_button.config(command=calculate_legacy)


# Funktion definieren, um die Eingaben auf Nummern zu prüfen
def validate_input(action, bool_if_allowed):
    if action == '1':
        if bool_if_allowed.isdigit() or bool_if_allowed == "":
            return True
        else:
            mainframe.bell()  # spielt einen nervigen ton ab, wenn man keine Zahl eingibt
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
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(1, weight=1)

# DropdownMenu um die Berechnungsmethode zu wechseln
calc_method = tk.StringVar()
calc_method_box = ttk.Combobox(mainframe, textvariable=calc_method, values=[
    "DevVersion", "Legacy"])
calc_method_box.bind("<<ComboboxSelected>>", change_calc_method)
calc_method_box.state(["readonly"])
calc_method.set("DevVersion")
calc_method_box.grid(column=0, row=0, sticky="W")

# Validate Input Funktion registrieren
validate_input_command = root.register(validate_input)

# Ausgabefenster erstellen
result_frame = tk.Text(mainframe, height=5, state="disabled")
result_frame.grid(column=0, row=1, columnspan=3,
                  sticky="NSEW", padx=(5, 0), pady=5)

# Scrollbar erstellen und mit Ausgabefenster verknüpfen
result_frame_scrollbar = ttk.Scrollbar(mainframe, command=result_frame.yview)
result_frame["yscrollcommand"] = result_frame_scrollbar.set
result_frame_scrollbar.grid(column=3, row=1, sticky="NS")

# Eingabefeld für den Wurzelexponenten
exponent = tk.StringVar()
expo_entry = ttk.Entry(mainframe, textvariable=exponent, validate="key", validatecommand=(validate_input_command, "%d",
                                                                                          "%P"))
expo_entry.grid(column=1, row=2, sticky="EW")

# Eingabefeld für den zu berechnenden Radikand
radikand = tk.StringVar()
radikand_entry = ttk.Entry(mainframe, textvariable=radikand)
radikand_entry.grid(column=1, row=3, sticky="EW")

# Eingabefeld für die Anzahl der Nachkommastellen
deci_places = tk.StringVar()
deci_places_entry = ttk.Entry(mainframe, textvariable=deci_places)
deci_places_entry.grid(column=1, row=4, sticky="EW")

# Beschriftung für die Eingabefelder erstellen und Ausrichten
expo_label = tk.Label(mainframe, text="Exponent")
expo_label.grid(column=0, row=2, sticky="E")

radi_label = tk.Label(mainframe, text="Radikand")
radi_label.grid(column=0, row=3, sticky="E")

deci_label = tk.Label(mainframe, text="Nachkommastellen")
deci_label.grid(column=0, row=4, sticky="E")

# Button für die Berechnung
calc_button = ttk.Button(mainframe, text="Berechnen!", command=calculate_dev)
calc_button.grid(column=2, row=3, sticky="W")

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
