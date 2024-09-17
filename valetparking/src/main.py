import math
import matplotlib.pyplot as plt
import numpy as np

num_personas = 1
tiempo_estancia_min = 15
tiempo_estancia_max = 30
t_llegadas = 20  # promedio de llegadas
total_espacios = 5  # el total de espacios para los clientes

# tiemposClientes = variable donde guardamos los tiempos de cada cliente es una arrary de objetos
# donde guardaremos la hora de llegada, tiempo del servicio, hora de salida, y tiempo de espera.
tiemposClientes = total_espacios * [{'llegada': 0, 'servicio': 0, 'salida': 0, 'espera': 0}]

te = 0.0  # tiempo de espera total
dt = 0.0  # duracion de servicio total
fin = 0.0  # minuto en el que finaliza

nRandoms = []  # arreglo donde se guardaran los numeros aleatorios


# funcion para obtener numero aleaotiros con la formula de congruencia lineal
# m,  el modulo
# a,  el multiplicador
# c,  el incremento
# X0 Valor inicial de la secuencia conocido como semilla
# noOfRandomNums, cantidad de numeros aleaotrios
def linear_Congruential_Method(Xo, a, c, m, noOfRandomNums):
    randomNums = [0] * (noOfRandomNums)  # se crea un arreglo de 0 con la lungitud de 0 a noOfRandomNums
    # noOfRandomNums = 5, entonces randomNums = [0,0,0,0,0]

    randomNums[0] = Xo  # en la primera posicion se guarda el valor de la semilla

    for i in range(1, noOfRandomNums):
        randomNums[i] = round(((randomNums[i - 1] * a) + c) % m,
                              4)  # formula de congruencia lineal para generar numeros pseudoaleatorios y cada valor lo guarda en randomNums[i]
        # round retorna el entero más cercano y 4 decimales
    return randomNums  # retornamos el arreglo con los numeros aleattorios


def estancia(cliente):
    global dt
    global nRandoms

    R = nRandoms[cliente]  # Obtiene un numero aleatorio de ese cliente y se guarda en R
    tiempo = tiempo_estancia_max - tiempo_estancia_min
    tiempo_estancia = tiempo_estancia_min + (tiempo * R)  # formula para calcular el tiempo de estancia del cliente
    tiemposClientes[cliente]['servicio'] = tiempo_estancia  # guardamos el tiempo de estancia
    print("Cliente %s utilizo el servicio %.2f minutos" % (cliente, tiempo_estancia))
    dt += tiempo_estancia  # se suma el tiempo de servicio
    return tiempo_estancia  # retornamos el tiempo de servicio


# funncion para determinar el minuto de llega y salida del cliente
def cliente(name):
    global te
    global fin
    global nRandoms

    cliente_llegada = tiemposClientes[name]['llegada']  # obtenemos el la hora de llegada
    print("---> Cliente %s llega al estacionamiento en minuto %.2f" % (name, cliente_llegada))

    espera = 0  # declaramos la varible espera, si es el primer cliente no tiene tiempo de espera
    if (name > 0):  # if para saber si es diferente del primer cliente
        # si no es el primer cliente se calcula si tuvo tiempo de espera
        if (tiemposClientes[name - 1]['salida'] > tiemposClientes[name]['llegada']):
            '''
            if para saber si la hora de salida del cliente anterior es mayor a la hora de llegada del cliente nuevo
            si la hora de salida es menor al tiempo de llegada quiere decir que no tuvo que esperar el cliente
            '''
            espera = tiemposClientes[name - 1]['salida'] - tiemposClientes[name][
                'llegada']  # se le resta la hora de llegada a la hora de salida del cliente anterior para calcular el tiempo de espera
            '''
            Ejemplo: si el cliente anterior salio al minuto 30 y el cliente nuevo llego al minuto 25 queire decir que espero 5 minitos
            30 - 25 = 5 minutos de espera

            '''

    tiemposClientes[name]['espera'] = espera
    te += espera  # se suman los tiempos de espera
    print("*** Cliente %s aparcan su auto habiendo esperado %.2f" % (name, espera))
    servicio = estancia(name)  # se ejecuta la funcion de estancia y se guarda en la variable servicio
    deja = servicio + cliente_llegada  # calculamos la hora de salida sumando el tiempo de servicio llegada
    tiemposClientes[name]['salida'] = deja  # guardamos la hora de salida
    print("<--- Cliente %s deja el estacionamiento en minuto %.2f" % (name, deja))
    fin = deja  # guardamos el valor en la variable fin para obtener la salida del ultimo cliente


if __name__ == "__main__":

    print("....Bienvenido....")

    llegada = 0  # inicializamos la varaible de llegada en 0
    i = 0

    # m,  el modulo
    # a,  el multiplicador
    # c,  el incremento
    # X0 Valor inicial de la secuencia conocido como semilla

    Xo = 0.8836
    m = 0.7
    a = 0.8
    c = 0.6

    xClientes = []
    yTiempoEspera = []
    yServicio = []
    nRandoms = linear_Congruential_Method(Xo, a, c, m, total_espacios)

    for i in range(total_espacios):  # se crea una se secuencia de numeros de 0 hasta total_espacios
        # "i" es el numero de cliente y siempre inicia en cero
        R = nRandoms[i]  # obtiene el numero aleatorio de la posicion i
        # math.log(R) -> calcular el logaritmo natural de R
        llegada += -t_llegadas * math.log(
            R)  # formula para calcular el tiempo de llegada y se acomula en la variable llegada
        tiemposClientes[i]['llegada'] = llegada  # guardamos la hora de llegada
        cliente(i)  # ejecutamos la funcion cliente y pasamos de parametro el numero de empleado
        print("\n")

        xClientes.append('Cliente ' + str(i))
        yTiempoEspera.append(tiemposClientes[i]['espera'])
        yServicio.append(tiemposClientes[i]['servicio'])

    # se calcula los promedios obtenidos del servicio total
    lpc = te / fin  # tiempo de espera total / la ultima salida del del cliente -> Longitud promedio de la cola
    print("\nLongitud promedio de cola: %.2f" % lpc)
    tep = te / total_espacios  # tiempo de espera total / total de espacios -> tiempo de espera promedio
    print("Tiempo de espera promedio = %.2f" % tep)
    upi = (dt / fin) / num_personas  # pocentaje que trabaja el valet parking
    print("Uso promedio del servicio 'Valet Parking' = %.2f" % upi)
    print("\n------------------------------------")

    # Grafica de tiempo de servicio y espera
    ind = np.arange(total_espacios)
    width = 0.35

    fig, ax = plt.subplots()

    p1 = ax.bar(ind, yTiempoEspera, width, label='Espera')
    p2 = ax.bar(ind, yServicio, width,
                bottom=yTiempoEspera, label='Servicio')

    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_ylabel('Minutos')
    ax.set_title('Grafica de tiempo de servicio y espera')
    ax.set_xticks(ind, labels=xClientes)
    ax.legend()

    # Label with label_type 'center' instead of the default 'edge'
    ax.bar_label(p1, label_type='center')
    ax.bar_label(p2, label_type='center')
    ax.bar_label(p2)

    plt.show()
