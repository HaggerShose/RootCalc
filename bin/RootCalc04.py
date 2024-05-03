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
            print(f"Berechnungszeit: {execution_time * 100:.3f} ms. ")


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
            while temp_result_int < radikand / 2:
                if temp_result_int**root_exponent == radikand:
                    formatted_result = "{:.{}f}".format(temp_result_int, deci_places)
                    end_time = time.time()
                    execution_time = end_time - start_time
                    return Decimal(formatted_result), execution_time
                else:
                    temp_result_int += step
            while step >= kill_condition:
                temp_result = result + 5 * step
                comp_value = temp_result**root_exponent
                if comp_value > radikand:
                    result, step = Algebra.root_calc_down(
                        radikand, root_exponent, step, temp_result
                    )
                elif comp_value < radikand:
                    result, step = Algebra.root_calc_up(radikand, root_exponent, step, temp_result)
                elif comp_value == radikand:  # Da stimmt etwas nicht
                    break
        formatted_result = "{:.{}f}".format(result, deci_places)
        end_time = time.time()
        execution_time = end_time - start_time
        return Decimal(formatted_result), execution_time

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
