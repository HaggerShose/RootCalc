import time
from decimal import Decimal, getcontext, DecimalException

radikand = 26
root_exponent = 2
deci_places = 2


def numeric_root_calc(radikand, deci_places, root_exponent):
    getcontext().prec = deci_places + 10  # +10 für Nötige Genauigkeit bei wenigen Nachkommastellen
    result = Decimal(5)
    step = Decimal(1)
    start_time = time.time()
    while True:
        if step < Decimal(1) / (10**deci_places):
            break
        temp_result = result**root_exponent
        if temp_result > radikand:
            result, step = root_calc_down(radikand, root_exponent, result, step)
        elif temp_result < radikand:
            result, step = root_calc_up(radikand, root_exponent, result, step)
        elif temp_result == radikand:
            break
    end_time = time.time()
    execution_time = end_time - start_time
    print(result)
    return result, execution_time


def root_calc_up(radikand, root_exponent, result, step):
    while True:
        temp_result = (result + step) ** root_exponent
        if temp_result < radikand:
            result += step
        elif temp_result == radikand:
            result += step
            return result, step
        else:
            step /= 10
            return result, step


def root_calc_down(radikand, root_exponent, result, step):
    while True:
        temp_result = result**root_exponent
        if temp_result > radikand:
            result -= step
        elif temp_result == radikand:
            return result, step
        else:
            step /= 10
            return result, step


numeric_root_calc(radikand, deci_places, root_exponent)
