import time
from decimal import Decimal, getcontext, DecimalException


class Algebra:
    @staticmethod
    def numeric_root_calc(radikand, deci_places, root_exponent):
        getcontext().prec = deci_places + 10
        result = Decimal(0)
        step = Decimal(1)

        start_time = time.time()

        while True:
            if root_exponent == 0:
                result = 1
                break
            elif step < Decimal(1) / (10**deci_places):
                break
            temp_result = (result + step) ** root_exponent
            if temp_result < radikand:
                result += step
            # elif temp_result > radikand:
            #    result -= step
            elif temp_result == radikand:
                result += step
                break
            else:
                step /= 10
        # Formatieren damit 0 an letzter Stelle angezeigt werden kann
        formatted_result = "{:.{}f}".format(result, deci_places)
        end_time = time.time()
        execution_time = end_time - start_time
        return Decimal(formatted_result), execution_time


class UserInput:
    @staticmethod
    def main():
        while True:
            user_input2 = input("Geben Sie den Wurzelexponenten ein: ").strip().lower()
            if user_input2 in ("exit", "e"):
                break
            elif not user_input2:
                continue
            try:
                if Decimal(user_input2) > 0:
                    pass
            except (ValueError, DecimalException):
                print("Falsche Eingabe, gib eine Zahl an")
                continue

            while True:
                user_input = input("Geben Sie den Radikand ein: ").strip().lower()
                if user_input in ("exit", "e"):
                    break
                elif not user_input2:
                    continue
                try:
                    if Decimal(user_input) > 0:
                        break
                except (ValueError, DecimalException):
                    print("Falsche Eingabe, gib eine Zahl an")
                    continue
            if user_input in ("exit", "e"):
                break

            while True:
                user_input1 = input("Wie viele Nachkommastellen soll das Ergebnis haben? ").strip().lower()
                if user_input1 in ("exit", "e"):
                    break
                elif not user_input2:
                    continue
                try:
                    if int(user_input1) >= 0:
                        break
                except ValueError:
                    print("Falsche Eingabe, gib eine ganze Zahl an")
                    continue
            if user_input1 in ("exit", "e"):
                break

            root_exponent = Decimal(user_input2)
            radikand = Decimal(user_input)
            deci_places = int(user_input1)
            final_result, execution_time = Algebra.numeric_root_calc(radikand, deci_places, root_exponent)

            print(
                f"Die {user_input2}-fache Wurzel von {radikand} mit {user_input1} Nachkommastellen ist: {final_result}"
            )
            print(f"Berechnungszeit: {execution_time * 1000:.3f} ms. ")


if __name__ == "__main__":
    UserInput.main()
