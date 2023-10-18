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
            except (ValueError, DecimalException):
                print("Falsche Eingabe, gib eine Zahl an")

    @staticmethod
    def main():
        print("\"e\" oder \"exit\" zum Beenden des Programms eingeben. ")
        while True:
            root_exponent = UserInput.get_numeric_input("Geben Sie den Wurzelexponenten ein: ")
            if root_exponent is None:
                return

            radikand = UserInput.get_numeric_input("Geben Sie einen Radikand ein: ")
            if radikand is None:
                return

            deci_places = int(UserInput.get_numeric_input("Wie viele Nachkommastellen soll das Ergebnis haben? "))
            if deci_places is None:
                return

            final_result, execution_time = Algebra.numeric_root_calc(radikand, deci_places, root_exponent)
            print(
                f"Die {root_exponent}-fache Wurzel von {radikand} mit {deci_places} "
                f"Nachkommastellen ist: {final_result}. ")
            print(f"Berechnungszeit: {execution_time * 100:.3f} ms. ")


class Algebra:
    @staticmethod
    def numeric_root_calc(radikand, deci_places, root_exponent):
        getcontext().prec = deci_places + 10  # +10 für Nötige Genauigkeit bei wenigen Nachkommastellen
        result = Decimal(5)
        step = Decimal(1)

        start_time = time.time()

        while True:
            if step < Decimal(1) / (10 ** deci_places):
                break
            temp_result = result ** root_exponent
            if temp_result > radikand:
                result, step = Algebra.root_calc_down(radikand, root_exponent, result, step)
            elif temp_result < radikand:
                result, step = Algebra.root_calc_up(radikand, root_exponent, result, step)
            elif temp_result == radikand:
                break
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time

    @staticmethod
    def root_calc_up(radikand, root_exponent, result, step):
        while True:
            temp_result = result ** root_exponent
            if temp_result < radikand:
                result += step
            elif temp_result == radikand:
                return result, step
            else:
                step /= 10
                return result, step

    @staticmethod
    def root_calc_down(radikand, root_exponent, result, step):
        while True:
            temp_result = result ** root_exponent
            if temp_result > radikand:
                result -= step
            elif temp_result == radikand:
                return result, step
            else:
                step /= 10
                return result, step


if __name__ == "__main__":
    UserInput.main()
