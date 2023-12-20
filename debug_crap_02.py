import time
from decimal import Decimal, getcontext, DecimalException

radikand = 13
root_exponent = 2
deci_places = 3
getcontext().prec = deci_places + 10
result = Decimal(0)
step = Decimal(1)
start_time = time.time()
while True:
    print(result)
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
end_time = time.time()
execution_time = end_time - start_time

print(result)
print(execution_time)