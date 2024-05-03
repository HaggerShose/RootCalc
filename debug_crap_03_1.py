from bin.RootCalc03_1 import Algebra


radikand = 5
root_exponent = 1
deci_places = 0

result, time = Algebra.numeric_root_calc(radikand, deci_places, root_exponent)

print(result)
print(time)
print("{:05.0f}".format(time * 1000))
