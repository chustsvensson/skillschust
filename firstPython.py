from turtle import Screen, Turtle
from math import *
import random
import time


def clic(x, y):

    global azules, blancos, nagono
    i, j = int(x), int(y)
    vprinc = check_ptos(i, j)
    if vprinc is None:
        return
    else:
        azules.append(vprinc)
        dib_dot(vprinc, "blue")
        burbuja(azules)

    if not nagono:
        crear_nagono(puntos.index(vprinc), nagono)

    if len(azules) < nbanderas:
        ver_ia = IA()
        blancos.append(ver_ia)
        dib_dot(ver_ia, "green")
        burbuja(blancos)
        cont1.clear()
        escribir_contador(str(nbanderas - len(azules)), "red", 90, 380)
    else:
        ver_ia = last_move()
        blancos.append(ver_ia)
        dib_dot(ver_ia, "green")
        burbuja(blancos)
        cont1.clear()
        escribir_contador(str(nbanderas - len(azules)), "red", 90, 380)

        ganador()
        pantalla.exitonclick()


def check_ptos(a, b):

    for punto in puntos:

        d = sqrt((punto[0] - a) ** 2 + (punto[1] - b) ** 2)

        if int(d) < 10 and check_disp(punto):
            return punto
    print("haz click en un círculo gris")


def check_disp(a):

    if a not in azules + blancos:
        return True
    else:
        return False


def crear_nagono(valor, poligono):

    paso = int(Numptos / nbanderas)
    for k in range(nbanderas):
        pos = rango(valor + k * paso)
        poligono.append(pos)


def arco(a, b):
    pos = rango(a + 1)
    while pos != b:
        if not check_disp(puntos[pos]):
            return False
        pos = rango(pos + 1)
    return True


def IA():

    temp = []
    for pos in nagono:
        if puntos[pos] not in azules + blancos:
            temp.append(pos)

    if temp:
        pos = random.choice(temp)
        return puntos[pos]

    for k in range(len(nagono)):

        a = nagono[k]
        if k + 1 == nbanderas:
            b = nagono[0]
        else:
            b = nagono[k+1]
        if puntos[a] in azules and puntos[b] in azules and arco(a, b):
            p = rango(a + 1)
            return puntos[p]

    marka = [0, 0]
    cont = 0
    conta = 0
    init = nagono[0]
    while conta < Numptos:
        pos = rango(init + 1)
        cont += 1
        while puntos[pos] not in azules:
            pos = rango(pos + 1)
            cont += 1

        a = init
        b = pos
        if arco(a, b) and abs(b - a) > 1 and abs(b-a) != Numptos - 1:

            if cont > marka[0]:
                marka[0] = cont
                marka[1] = rango(a + 1)

        init = b
        conta += cont
        cont = 0
    if marka[0] != 0:
        return puntos[marka[1]]

    colores = [azules, blancos]
    color = 0
    init = nagono[0]
    marca = [0, 0]
    cont = 0
    conta = 0
    while conta <= Numptos:
        pos = rango(init + 1)
        cont += 1
        while puntos[pos] not in azules + blancos:
            pos = rango(pos + 1)
            cont += 1
        if puntos[pos] not in colores[color]:
            a = init
            b = pos
            if arco(a, b) and abs(b - a) > 1 and abs(b - a) != Numptos - 1:
                if color == 0:
                    color = 1
                    if cont > marca[0]:
                        marca[0] = cont
                        marca[1] = rango(a + 1)
                elif color == 1:
                    color = 0
                    if cont > marca[0]:
                        marca[0] = cont
                        marca[1] = rango(b - 1)
            else:
                if color == 0:
                    color = 1
                else:
                    color = 0
        init = pos
        conta += cont
        cont = 0
        if marca[0] != 0:
            return puntos[marca[1]]

    for punto in puntos:
        if punto not in azules + blancos:
            return punto


def burbuja(lista):

    temp = []
    for par in lista:
        pos = puntos.index(par)
        temp.append(pos)

    for i in range(1, len(temp)):
        for j in range(0, len(temp) - 1):
            if temp[j] > temp[j + 1]:
                elemento = temp[j]
                elemento2 = lista[j]
                temp[j] = temp[j + 1]
                lista[j] = lista[j + 1]
                temp[j+1] = elemento
                lista[j+1] = elemento2


def dib_dot(pto, color):
    tortuga.penup()
    tortuga.goto(pto)
    tortuga.pendown()
    tortuga.dot(20, color)
    tortuga.penup()
    tortuga.home()


def rango(valor):
    if valor > Numptos - 1:
        valor = valor - Numptos
        return valor
    else:
        return valor


def arko(inic, final, color):
    if color == 0:
        color = "blue"
    else:
        color = "green"
    p = rango(inic + 1)
    while p != final:
        dib_dot(puntos[p], color)
        p = rango(p + 1)


def ganador():
    colores = [azules, blancos]

    areas = [0, 0]
    color = 0
    init = nagono[0]
    cont = 0
    pasos = 0

    while pasos < Numptos:
        pos = rango(init + 1)
        cont += 1
        while puntos[pos] not in azules + blancos:
            pos = rango(pos + 1)
            cont += 1
        if puntos[pos] in colores[color]:
            k = rango(init + 1)
            while k != pos:
                colores[color].append(puntos[k])
                k = rango(k + 1)
            areas[color] += cont
            dib_sector(puntos[init], puntos[pos], color)
            arko(init, pos, color)

        else:
            if color == 0:
                color = 1
            else:
                color = 0

        init = pos
        pasos += cont
        cont = 0

    if len(azules) > len(blancos):
        escribir_pantalla("Gana jugador", "red", -60, -400)
    elif len(azules) < len(blancos):
        escribir_pantalla("Gana IA", "red", -60, -400)
    else:
        escribir_pantalla("Es un empate", "red", -60, -400)
    return


def last_move():

    for k in range(len(nagono)):
        a = nagono[k]
        if k + 1 == nbanderas:
            b = nagono[0]
        else:
            b = nagono[k+1]
        if puntos[a] in blancos and puntos[b] in blancos:
            if arco(a, b):
                marka = [0, 0]
                cont = 0
                conta = 0
                init = nagono[0]
                while conta < Numptos:
                    pos = rango(init + 1)
                    cont += 1
                    while puntos[pos] not in azules:
                        pos = rango(pos + 1)
                        cont += 1
                    a = init
                    b = pos
                    if arco(a, b) and abs(b - a) > 1 and abs(b-a) != Numptos - 1:
                        if cont > marka[0]:
                            marka[0] = cont
                            marka[1] = rango(a + 1)

                    init = b
                    conta += cont
                    cont = 0
                if marka[0] != 0:
                    return puntos[marka[1]]

    colores = [azules, blancos]
    color = 0
    init = nagono[0]
    marca = [0, 0]
    cont = 0
    conta = 0
    while conta <= Numptos:
        pos = rango(init + 1)
        cont += 1
        while puntos[pos] not in azules + blancos:
            pos = rango(pos + 1)
            cont += 1
        if puntos[pos] not in colores[color]:
            a = init
            b = pos
            if arco(a, b) and abs(b - a) > 1 and abs(b - a) != Numptos - 1:
                if color == 0:
                    color = 1

                    if cont > marca[0]:
                        marca[0] = cont
                        marca[1] = rango(a + 1)
                elif color == 1:
                    color = 0

                    if cont > marca[0]:
                        marca[0] = cont
                        marca[1] = rango(b - 1)
            else:
                if color == 0:
                    color = 1
                else:
                    color = 0
        init = pos
        conta += cont
        cont = 0
    if marca[0] != 0:
        return puntos[marca[1]]
    else:
        for punto in puntos:
            if punto not in azules + blancos:
                return punto


def dib_sector(a, b, color):
    if color == 0:
        valor = "blue"
    elif color == 1:
        valor = "green"

    tortuga.color(valor)
    tortuga.pensize(3)

    tortuga.penup()
    tortuga.goto(b)
    tortuga.pendown()

    tortuga.goto(0, 0)
    tortuga.goto(a)
    tortuga.penup()


def escribir_pantalla(texto, color, X, Y):
    tortuga.penup()
    tortuga.goto(X, Y)
    tortuga.pendown()
    tortuga.color(color)
    tortuga.write(texto, font=("Arial", 15, "normal"))
    tortuga.penup()
    tortuga.home()
    tortuga.pendown()
    return


def escribir_contador(texto, color, X, Y):
    cont1.penup()
    cont1.goto(X, Y)
    cont1.pendown()
    cont1.color(color)
    cont1.write(texto, font=("Arial", 15, "bold"))
    cont1.penup()
    cont1.home()
    cont1.pendown()
    return


pantalla = Screen()
pantalla.setup(1025, 1025)
pantalla.screensize(1000, 1000)
pantalla.setworldcoordinates(-500, -500, 500, 500)
pantalla.delay(0)

tortuga = Turtle()
tortuga.speed(0)

cont1 = Turtle("blank")
cont1.color("red")
cont1.speed(0)


# número de banderas para cada jugador
nbanderas = 10

# radio de la circunferencia del territorio a disputar
R = 350
azules = []
blancos = []
puntos = []
nagono = []

# divisiones de la circunferencia según número de puntos
Numptos = 100
alfa = 0
beta = 2 * pi / Numptos
for k in range(Numptos):
    x = int(R * cos(alfa))
    y = int(R * sin(alfa))
    puntos.append((x, y))
    alfa += beta


tortuga.hideturtle()
tortuga.pensize(2)
tortuga.penup()
tortuga.goto(0, -R)
tortuga.pendown()
tortuga.circle(R)
tortuga.penup()
tortuga.home()


for punto in puntos:
    dib_dot(punto, "grey")

escribir_pantalla("DISPUTA DE TERRITORIO", "black", -100, 460)
escribir_pantalla("Primero coloca bandera el jugador y después la IA", "black", -200, 420)
escribir_pantalla(" Banderas a colocar ", "black", -100, 380)
escribir_contador(str(nbanderas - len(azules)), "red", 90, 380)
pantalla.onclick(clic)

pantalla.mainloop()

