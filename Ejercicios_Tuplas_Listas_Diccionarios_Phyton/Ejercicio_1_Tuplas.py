# Ejercicio 1: Tuplas

vulnerabilidades = ('SQL Injection', 'Cross-Site Scripting', 'Buffer Overflow', 'Denegación de Servicio')
print(vulnerabilidades[1])
print(vulnerabilidades[-2:])
try:
    vulnerabilidades[0] = 'Otro'
except TypeError as e:
    print(e)
