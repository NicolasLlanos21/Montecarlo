import random
from scipy.stats import norm

# Parámetros del generador lineal congruencial
a = 1664525                         #Pendiente  = {a E Z | 1 <= a < m}
c = 1013904223                      #Intersección = {c E Z | 0 <= C < m} 
m = 2**32                           #Conjunto = {m E Z | m > 0} 
semilla = 1                         #Semilla -> [0,m)  = {Xo E Z | 0 <= Xo < m}
ri = []                             #Numeros Ri
ni = []                             #Numeros Ni


# Función para generar Ri con congruencia Lineal
def generar_ri(semilla,n):   
    ri.clear()    
    if semilla is None:
        semilla = random.randint(0, m - 1)  #Semilla -> [0,m)  = {Xo E Z | 0 <= Xo < m} se utiliza unicamente para generar una semilla si no se especifica una
        
    for _ in range(n):
        semilla = (a * semilla + c) % m
        ri.append(semilla / (m - 1))    


def generarDistrNormal(n, media, desviacion_estandar):
    global ni
    ni = []
    semilla = None
    generar_ri(semilla, n)
    ni += [round(norm.ppf(numero, loc=media, scale=desviacion_estandar), 5) for numero in ri]    
    # Calcular la inversa de la distribución normal para cada número pseudoaleatorio y redondear a 5 decimales
    return ni[0]

def generarIntDistrNormal(n, media, desviacion_estandar):
    global ni
    ni = []
    semilla = None
    generar_ri(semilla, n)
    ni += [round(norm.ppf(numero, loc=media, scale=desviacion_estandar)) for numero in ri]    
    # Calcular la inversa de la distribución normal para cada número pseudoaleatorio y redondear al entero más cercano
    return ni[0]
