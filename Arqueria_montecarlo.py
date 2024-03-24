import plotly.graph_objects as go
import copy
import uniforme
import normal

class Arquero:
    def __init__(self, genero, nombre, res):
        self.genero = genero
        self.nombre = nombre
        self.resistencia_gen = res
        self.resistencia = res
        self.resistencia_actual = res
        self.experiencia = 0
        self.suerte = uniforme.generarDistrUniforme(3,1,1)
        self.puntaje = 0 
        self.lanzamientos_extra_consecutivos = 0

    def lanzamiento(self):
        precision = uniforme.generarDistrUniforme(1,0,1)
        if self == 'mujer':
            if precision <= 0.38:
                diana = 'central'
                puntaje = 10
            elif precision <= 0.68:
                diana = 'intermedia'
                puntaje = 9
            elif precision <= 0.95:
                diana = 'exterior'
                puntaje = 8
            else:
                diana = 'fallo'
                puntaje = 0
        else:  # Si es hombre
            if precision <= 0.20:
                diana = 'central'
                puntaje = 10
            elif precision <= 0.53:
                diana = 'intermedia'
                puntaje = 9
            elif precision <= 0.93:
                diana = 'exterior'
                puntaje = 8
            else:
                diana = 'fallo'
                puntaje = 0

        return diana, puntaje
            
class Simulacion:
    def __init__(self, equipo1, equipo2):
        self.equipo1 = equipo1
        self.equipo2 = equipo2

    def actualizar_suerte(self):
        # Actualizar suerte de los arqueros en ambos equipos
        for arquero in self.equipo1.arqueros:
            arquero.suerte = uniforme.generarDistrUniforme(3,1,1)
        for arquero in self.equipo2.arqueros:
            arquero.suerte = uniforme.generarDistrUniforme(3,1,1)
        
    def realizar_ronda(self):
        # Actualizar suerte al inicio de la ronda
        self.actualizar_suerte()
        # Inicializar registros de equipos y jugadores
        registros_equipo1 = []
        registros_equipo2 = []
        # Inicializar contadores de lanzamientos extra consecutivos ganados por cada arquero
        lanzamientos_extra_consecutivos_equipo1 = 0
        lanzamientos_extra_consecutivos_equipo2 = 0
        # Realizar lanzamientos hasta que la resistencia de todos los arqueros se agote
        while True:
            resistencia_agotada = True
            # Realizar lanzamientos para el Equipo 1
            for arquero in self.equipo1.arqueros:
                if arquero.resistencia >= 5:
                    resistencia_agotada = False
                    diana, puntaje = arquero.lanzamiento()
                    arquero.resistencia -= 5
                    arquero.puntaje += puntaje
                    registros_equipo1.append((arquero, diana, puntaje))

            # Realizar lanzamientos para el Equipo 2
            for arquero in self.equipo2.arqueros:
                if arquero.resistencia >= 5:
                    resistencia_agotada = False
                    diana, puntaje = arquero.lanzamiento()
                    arquero.resistencia -= 5
                    arquero.puntaje += puntaje
                    registros_equipo2.append((arquero, diana, puntaje))

            # Si todos los arqueros tienen resistencia menor a 5, terminar la ronda
            if resistencia_agotada:
                break

        # Determinar arquero con más suerte en cada equipo para lanzamiento extra
        max_suerte_equipo1 = max(self.equipo1.arqueros, key=lambda arquero: arquero.suerte)
        max_suerte_equipo2 = max(self.equipo2.arqueros, key=lambda arquero: arquero.suerte)
        
        if max_suerte_equipo1.suerte > max_suerte_equipo2.suerte:
            arquero_con_mas_suerte = max_suerte_equipo1
        else:
            arquero_con_mas_suerte = max_suerte_equipo2

        # Realizar lanzamiento extra para el arquero con más suerte de cada equipo
        if uniforme.generarIntDistrUniforme(2,1,1) == 1:
            diana, puntaje_extra = max_suerte_equipo1.lanzamiento()
            registros_equipo1.append((max_suerte_equipo1, diana, puntaje_extra))
            if puntaje_extra > 0:
                lanzamientos_extra_consecutivos_equipo1 += 1
            else:
                lanzamientos_extra_consecutivos_equipo1 = 0
        if uniforme.generarIntDistrUniforme(2,1,1) == 1:
            diana, puntaje_extra = max_suerte_equipo2.lanzamiento()
            registros_equipo2.append((max_suerte_equipo2, diana, puntaje_extra))
            if puntaje_extra > 0:
                lanzamientos_extra_consecutivos_equipo2 += 1
            else:
                lanzamientos_extra_consecutivos_equipo2 = 0

        # Si un jugador gana tres lanzamientos extra consecutivos, tiene derecho a un lanzamiento extra
        if lanzamientos_extra_consecutivos_equipo1 == 3:
            diana, puntaje_extra = max_suerte_equipo1.lanzamiento()
            registros_equipo1.append((max_suerte_equipo1,  diana, puntaje_extra))
            # Se agrega el puntaje extra al equipo pero no al puntaje individual del arquero
            self.equipo1.puntaje += puntaje_extra if puntaje_extra > 0 else 0
            lanzamientos_extra_consecutivos_equipo1 = 0  # Reiniciar el contador de lanzamientos extra

        if lanzamientos_extra_consecutivos_equipo2 == 3:
            diana, puntaje_extra = max_suerte_equipo2.lanzamiento()
            registros_equipo2.append((max_suerte_equipo2, diana, puntaje_extra))
            # Se agrega el puntaje extra al equipo pero no al puntaje individual del arquero
            self.equipo2.puntaje += puntaje_extra if puntaje_extra > 0 else 0
            lanzamientos_extra_consecutivos_equipo2 = 0  # Reiniciar el contador de lanzamientos extra

        # Determinar ganador de la ronda
        puntaje_equipo1 = sum(puntaje for _, _, puntaje in registros_equipo1)
        puntaje_equipo2 = sum(puntaje for _, _,puntaje in registros_equipo2)

        if puntaje_equipo1 > puntaje_equipo2:
            ganador = 1
        elif puntaje_equipo1 < puntaje_equipo2:
            ganador = 2
        else:
            ganador = 0

        # Determinar arquero con más puntos en cada equipo
        arquero_ganador_equipo1 = max(self.equipo1.arqueros, key=lambda arquero: arquero.puntaje)
        arquero_ganador_equipo2 = max(self.equipo2.arqueros, key=lambda arquero: arquero.puntaje)

        # Determinar cuál de los dos arqueros ganadores tiene más puntos
        if arquero_ganador_equipo1.puntaje > arquero_ganador_equipo2.puntaje:
            arquero_con_mas_puntos = arquero_ganador_equipo1
        else:
            arquero_con_mas_puntos = arquero_ganador_equipo2
            
        # Sumar 3 puntos de experiencia al arquero con más puntos
        arquero_con_mas_puntos.experiencia += 3
        
                # Actualizar resistencia de los arqueros al final de la ronda
        for arquero in self.equipo1.arqueros + self.equipo2.arqueros:
            if arquero.experiencia > 9:
                arquero.resistencia = max(0, arquero.resistencia_actual - 1)
                arquero.resistencia_actual = max(0, arquero.resistencia)
            else:
                arquero.resistencia = max(0, arquero.resistencia_actual - uniforme.generarIntDistrUniforme(2,1,1))
                arquero.resistencia_actual = max(0, arquero.resistencia)

        return ganador, registros_equipo1, registros_equipo2, copy.deepcopy(arquero_con_mas_puntos), copy.deepcopy(arquero_con_mas_suerte)
        
    def reiniciarPuntos(self):
        for arquero in self.equipo1.arqueros:
            arquero.puntaje = 0    
            arquero.resistencia = arquero.resistencia_gen
            arquero.resistencia_actual = arquero.resistencia_gen
        for arquero in self.equipo2.arqueros:
            arquero.puntaje = 0    
            arquero.resistencia = arquero.resistencia_gen
            arquero.resistencia_actual = arquero.resistencia_gen
        return
    
    def reiniciar_exp(self):
        for arquero in self.equipo1.arqueros:
            arquero.experiencia = 0
        for arquero in self.equipo2.arqueros:
            arquero.experiencia = 0

    def obtener_arquero_mas_suerte(self,resultados_partido):
        # Diccionario para almacenar la suma acumulada de suerte de cada arquero
        sumas_suerte_arqueros = {}
        
        for _, _, _,_,arqueroMaxSuerte in resultados_partido:
            if arqueroMaxSuerte not in sumas_suerte_arqueros:
                sumas_suerte_arqueros[arqueroMaxSuerte] = 0
                sumas_suerte_arqueros[arqueroMaxSuerte] += arqueroMaxSuerte.suerte
            
        # Encontrar el arquero con la mayor suma de suerte
        arquero_mas_suerte = max(sumas_suerte_arqueros, key=sumas_suerte_arqueros.get)
        suerte_maxima = sumas_suerte_arqueros[arquero_mas_suerte]

        return arquero_mas_suerte, suerte_maxima
    
    def obtener_arqueros_mas_suerte_total(self,resultados_simulacion):
        arqueros_mas_suerte = []
        suertes_maximas = []
        for resultados_partido in resultados_simulacion:
            arquero_mas_suerte, suerte_maxima = simulacion.obtener_arquero_mas_suerte(resultados_partido)
            arqueros_mas_suerte.append(arquero_mas_suerte.nombre)
            suertes_maximas.append(suerte_maxima)
        return arqueros_mas_suerte,suertes_maximas

    def obtener_arquero_mas_experiencia(self):
        # Diccionario para almacenar la experiencia acumulada de cada arquero
        sumas_experiencia_arqueros = {}

        # Iterar sobre los arqueros del equipo 1 y acumular la experiencia de cada arquero
        for arquero in self.equipo1.arqueros:
            if arquero.nombre not in sumas_experiencia_arqueros:
                sumas_experiencia_arqueros[arquero.nombre] = 0
            sumas_experiencia_arqueros[arquero.nombre] += arquero.experiencia

        # Iterar sobre los arqueros del equipo 2 y acumular la experiencia de cada arquero
        for arquero in self.equipo2.arqueros:
            if arquero.nombre not in sumas_experiencia_arqueros:
                sumas_experiencia_arqueros[arquero.nombre] = 0
            sumas_experiencia_arqueros[arquero.nombre] += arquero.experiencia

        # Encontrar el arquero con la mayor experiencia acumulada
        arquero_mas_experiencia = max(sumas_experiencia_arqueros, key=sumas_experiencia_arqueros.get)
        experiencia_maxima = sumas_experiencia_arqueros[arquero_mas_experiencia]

        return arquero_mas_experiencia, experiencia_maxima

    def obtener_genero_mas_victorias_partido(self, resultados_partido):
        visctorias_por_genero_totales = {'Masculino': 0, 'Femenino': 0}
        
        for _, _, _,arqueroMaxPuntos,_ in resultados_partido:
            visctorias_por_genero_totales[arqueroMaxPuntos.genero] += 1

        arquero_mas_victorias = max(visctorias_por_genero_totales, key=visctorias_por_genero_totales.get)
        victorias = visctorias_por_genero_totales[arquero_mas_victorias]
            
        return arquero_mas_victorias, victorias
    
    def obtener_genero_mas_puntos_juego(self, resultados_partido):
        genero_mas_puntos_por_juego = []
        visctorias_por_genero_totales = {'Masculino': 0, 'Femenino': 0}
        
        for resultados_juego in resultados_partido:
            genero_mas_victorias, victorias = simulacion.obtener_genero_mas_victorias_partido(resultados_juego)
            genero_mas_puntos_por_juego.append((genero_mas_victorias,victorias))
            visctorias_por_genero_totales[genero_mas_victorias] += 1
        
        return genero_mas_puntos_por_juego, visctorias_por_genero_totales      
            
    def determinar_equipo_ganador(self, resultados_partido):
        puntaje_equipo1 = 0
        puntaje_equipo2 = 0
        for resultados_juego in resultados_partido:
            for _, registros_equipo1, registros_equipo2,_,_ in resultados_juego:
                for _, _, puntaje in registros_equipo1:
                    puntaje_equipo1 += puntaje
                for _, _, puntaje in registros_equipo2:
                    puntaje_equipo2 += puntaje

            if puntaje_equipo1 > puntaje_equipo2:
                ganador = 1
                puntaje_ganador = puntaje_equipo1
            elif puntaje_equipo1 < puntaje_equipo2:
                ganador = 2
                puntaje_ganador = puntaje_equipo2
            else:
                ganador = None
                puntaje_ganador = puntaje_equipo1

        return ganador, puntaje_ganador

    def obtener_puntos_jugadores(self,resultados_por_juego):
        puntajes_jugadores = []
        # Iterar sobre los resultados de cada juego
        for resultados_partido in resultados_por_juego:
            puntajeJuego = 0
            for _,registros_equipo1, registros_equipo2,_,_ in resultados_partido:
                # Obtener nombres y puntajes de los jugadores del equipo 1
                for _, _, puntaje in registros_equipo1:
                    puntajeJuego += puntaje
                # Obtener nombres y puntajes de los jugadores del equipo 2
                for _, _, puntaje in registros_equipo2:
                    puntajeJuego += puntaje
            puntajes_jugadores.append(puntajeJuego)
            puntajeJuego = 0
        return puntajes_jugadores

    def graficar_puntajes_totales_jugadores(self,puntajes_jugadores):
        fig = go.Figure()
        # Barras
        fig.add_trace(go.Bar(x=list(range(1, len(puntajes_jugadores) + 1)), y=puntajes_jugadores,
                            marker_color='purple'))

        # Diseño del gráfico
        fig.update_layout(title='Puntaje total de todos los jugadores por juego',
                        xaxis_title='Número del juego',
                        yaxis_title='Puntaje total',
                        xaxis=dict(type='linear'),
                        yaxis=dict(type='linear'),
                        )
        # Mostrar el gráfico
        fig.show()
        
    def graficar_suerte_juego(self,arqueros_mas_suerte,suertes_maximas):
        # Convertir el rango a lista para Plotly para X
        num_partidos = list(range(1, len(arqueros_mas_suerte) + 1))
        # Crear el gráfico de barras
        fig = go.Figure([go.Bar(x=num_partidos, y=suertes_maximas, text=arqueros_mas_suerte)])

        # Establecer etiquetas y título
        fig.update_layout(title='Arquero con más suerte por Juego',
                        xaxis_title='Partido',
                        yaxis_title='Suerte acumulada')

        # Mostrar el gráfico
        fig.show()
        
    def graficar_exp_juego(self,arqueros_mas_exp,exp_maximas):
            # Convertir el rango a lista para Plotly para X
            num_partidos = list(range(1, len(arqueros_mas_exp) + 1))
            # Crear el gráfico de barras
            fig = go.Figure([go.Bar(x=num_partidos, y=exp_maximas, text=arqueros_mas_exp)])

            # Establecer etiquetas y título
            fig.update_layout(title='Arquero con más experencia por juego',
                            xaxis_title='Partido',
                            yaxis_title='Experiencia acumulada')

            # Mostrar el gráfico
            fig.show()
            
    def graficar_ganadores_genero(self,genero_mas_puntos_por_juego, puntajes_por_genero):
        juegos = list(range(1, len(genero_mas_puntos_por_juego) + 1))
        # Graficar Victorias totales por género
        fig = go.Figure(data=[go.Bar(x=list(puntajes_por_genero.keys()), y=list(puntajes_por_genero.values()),
                                    marker_color=['blue', 'pink'])])
        fig.update_layout(title='Victorias totales por género', xaxis_title='Género', yaxis_title='Puntaje total')
        fig.show()

        # Graficar Victorias de cada genero por juego
        fig = go.Figure()
        # Agregar barras para los puntajes por juego
        for juego, (genero, puntaje) in zip(juegos, genero_mas_puntos_por_juego):
            color = 'blue' if genero == 'Masculino' else 'pink'
            fig.add_trace(go.Bar(x=[juego], y=[puntaje],name=genero ,marker_color=color))
        # Establecer etiquetas y título
        fig.update_layout(title='Victorias de cada genero por juego',
                        xaxis_title='Juego',
                        yaxis_title='Puntaje total')
        # Mostrar la figura
        fig.show()
        return
    
class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.arqueros = []
        self.registros_por_ronda = []  # Registros por ronda para cada arquero

    def agregar_arquero(self, arquero):
        self.arqueros.append(arquero)
            

equipo1 = Equipo("Equipo 1")
equipo2 = Equipo("Equipo 2")

# Agregar arqueros a los equipos
for i in range(5):
    generos = ["Femenino", "Masculino"]
    genero_arquero1 = uniforme.generarDistrUniforme(1, 0, 1)
    genero_elegido_arquero1 = generos[0] if genero_arquero1 < 0.5 else generos[1]
    genero_arquero2 = uniforme.generarDistrUniforme(1, 0, 1)
    genero_elegido_arquero2 = generos[0] if genero_arquero1 < 0.5 else generos[1]
    arquero1 = Arquero(genero_elegido_arquero1, "Arquero 1-" + str(i+1),normal.generarIntDistrNormal(1,35,10))
    arquero2 = Arquero(genero_elegido_arquero2, "Arquero 2-" + str(i+1),normal.generarIntDistrNormal(1,35,10))
    equipo1.agregar_arquero(arquero1)
    equipo2.agregar_arquero(arquero2)

# Crear simulación
simulacion = Simulacion(equipo1, equipo2)

def realizarJuego(equipo1, equipo2):
        resultados_partido = []
        for i in range(10):
            ganador, registros_equipo1, registros_equipo2, arqueroMaxPuntos, ArqueroMaxSuerte, = simulacion.realizar_ronda()             
            resultados_partido.append((ganador, registros_equipo1, registros_equipo2,arqueroMaxPuntos,ArqueroMaxSuerte))
        return resultados_partido
    
arqueros_mas_exp = []
exp_maximas = []

def obtener_arqueros_max_exp_juego():
    arquero_mas_experiencia, experiencia_maxima = simulacion.obtener_arquero_mas_experiencia()
    arqueros_mas_exp.append(arquero_mas_experiencia)
    exp_maximas.append(experiencia_maxima)
    
def realizarJuegos(equipo1,equipo2,total):
    resutados = []
    for i in range(total):
        resutados.append(realizarJuego(equipo1,equipo2))
        obtener_arqueros_max_exp_juego()
        simulacion.reiniciarPuntos()
        simulacion.reiniciar_exp()
    return resutados
#-------------------------------------------------------SIMULACION-------------------------------------------------------------------------
# Realizar Juego
print("Pensando...")
resultados_simulacion = realizarJuegos(equipo1,equipo2,20000)
print("Graficando...")

#Obtener arqueros con mas suerte
arqueros_mas_suerte,suertes_maximas = simulacion.obtener_arqueros_mas_suerte_total(resultados_simulacion)    
simulacion.graficar_suerte_juego(arqueros_mas_suerte,suertes_maximas)

#Obtener arqueros con mas experiencia
simulacion.graficar_exp_juego(arqueros_mas_exp,exp_maximas)

#genero con mas Victorias
genero_mas_puntos_por_juego, puntajes_por_genero = simulacion.obtener_genero_mas_puntos_juego(resultados_simulacion)
simulacion.graficar_ganadores_genero(genero_mas_puntos_por_juego, puntajes_por_genero)

#Obtener el puntaje total de cada jugador en cada juego
puntaje_jugadores =  simulacion.obtener_puntos_jugadores(resultados_simulacion)
simulacion.graficar_puntajes_totales_jugadores(puntaje_jugadores)

#Determinar equipo ganador
ganador, puntaje_ganador =  simulacion.determinar_equipo_ganador(resultados_simulacion)
print("Gana el Juego el equipo: " + str(ganador) + " con " + str(puntaje_ganador) + " puntos")
