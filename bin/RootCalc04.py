import time
from decimal import Decimal, getcontext, DecimalException


class UserInput:
    @staticmethod
    def get_numeric_input(prompt):
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in ("exit", "e"):
                return None
            elif not user_input:
                continue
            try:
                value = Decimal(user_input)
                if value >= 0:
                    return value
                else:
                    print("Falsche Eingabe, gib eine positive Zahl an")
            except (ValueError, DecimalException):
                print("Falsche Eingabe, gib eine Zahl an")

    @staticmethod
    def get_root_exponent_input(prompt):
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in ("exit", "e"):
                return None
            elif not user_input:
                continue
            try:
                value = Decimal(user_input)
                return value
            except (ValueError, DecimalException):
                print("Falsche Eingabe, gib eine Zahl an")

    @staticmethod
    def main():
        print('"e" oder "exit" zum Beenden des Programms eingeben. ')
        while True:
            root_exponent = UserInput.get_root_exponent_input(
                "Geben Sie den Wurzelexponenten ein: "
            )
            if root_exponent is None:
                return

            radikand = UserInput.get_numeric_input("Geben Sie einen Radikand ein: ")
            if radikand is None:
                return

            deci_places = int(
                UserInput.get_numeric_input("Wie viele Nachkommastellen soll das Ergebnis haben? ")
            )
            if deci_places is None:
                return

            final_result, execution_time = Algebra.numeric_root_calc(
                radikand, deci_places, root_exponent
            )
            print(
                f"Die {root_exponent}-fache Wurzel von {radikand} mit {deci_places} "
                f"Nachkommastellen ist: {final_result}. "
            )
            print(f"Berechnungszeit: {execution_time} ms. ")


class Algebra:
    @staticmethod
    def numeric_root_calc(radikand, deci_places, root_exponent):
        getcontext().prec = (
            deci_places + 10
        )  # +10 für nötige Genauigkeit bei wenigen Nachkommastellen
        result = Decimal(0)
        step = Decimal(1)
        kill_condition = Decimal(1) / (10**deci_places)
        start_time = time.time()
        # Behandle negative Exponenten
        if root_exponent < 0:
            # Berechne die Wurzel mit dem positiven Exponenten und invertiere das Ergebnis
            positive_exponent = abs(root_exponent)
            positive_result, _ = Algebra.numeric_root_calc(radikand, deci_places, positive_exponent)
            result = Decimal(1) / positive_result
        # Schleifen zur Berechnung
        else:
            # Sonderfälle
            while step >= kill_condition:
                if root_exponent == 0:
                    result = 1
                    break
                elif root_exponent == 1:
                    result = radikand
                    break
                elif radikand == 0:
                    result = 0
                    break
                elif radikand == 1:
                    result = 1
                    break
                temp_result_int = result
                # Abkürzung um bei ganzzahligen Ergebnissen nicht n NachkommaNullen berechnen zu lassen
                while temp_result_int < radikand / 2:
                    if temp_result_int**root_exponent == radikand:
                        end_time = time.time()
                        execution_time = end_time - start_time
                        formatted_exe_time = "{:05.0f}".format(execution_time * 1000)
                        formatted_result = "{:.{}f}".format(temp_result_int, deci_places)
                        return Decimal(formatted_result), formatted_exe_time
                    else:
                        temp_result_int += step
                # Hauptschleife zur Berechnung
                while step >= kill_condition:
                    temp_result = result + 5 * step
                    comp_value = temp_result**root_exponent
                    if comp_value > radikand:
                        result, step = Algebra.root_calc_down(
                            radikand, root_exponent, step, temp_result
                        )
                    elif comp_value < radikand:
                        result, step = Algebra.root_calc_up(
                            radikand, root_exponent, step, temp_result
                        )
                    elif comp_value == radikand:  # Da stimmt etwas nicht
                        break

        end_time = time.time()
        execution_time = end_time - start_time
        formatted_exe_time = "{:05.0f}".format(execution_time * 1000)
        formatted_result = "{:.{}f}".format(result, deci_places)
        return Decimal(formatted_result), formatted_exe_time

    # Methoden um Nachkommastellen zu Addieren oder Subtrahieren
    @staticmethod
    def root_calc_up(radikand, root_exponent, step, temp_result):
        while True:
            temp_result_up = (temp_result + step) ** root_exponent
            if temp_result_up < radikand:
                temp_result += step
            elif temp_result_up == radikand:
                temp_result += step
                return temp_result, step
            else:
                step /= 10
                return temp_result, step

    @staticmethod
    def root_calc_down(radikand, root_exponent, step, temp_result):
        while True:
            temp_result_up = (temp_result - step) ** root_exponent
            if temp_result_up > radikand:
                temp_result -= step
            elif temp_result_up == radikand:
                temp_result -= step
                step /= 10
                return temp_result, step
            else:
                temp_result -= step
                step /= 10
                return temp_result, step


if __name__ == "__main__":
    UserInput.main()
