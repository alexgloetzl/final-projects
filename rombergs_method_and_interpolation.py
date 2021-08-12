# -*- coding: utf-8 -*-
"""
# Abgabe Projektarbeit Einführung ins Programmieren mit Python
# Projekt:
#     Das Romberg-Verfahren
# Name:
#     Alexander Glötzl, Mat.Nr. 1627077
# Bemerkung:
#     benotet    
"""
import math
import numpy as np
import matplotlib.pyplot as plt

def func_test(x):
    y = x*math.cos(x) + math.exp(x)
    return y

def gravity(x, m = 10):                                                       #masse m = 10kg
    y = -9.81*m
    return y

def romberg(func, a, b, epsilon = 1e-3, ausgabe = 1):                         #bei default ausgabe = 1, dann soll eine "schöne" Dreiecksmatrix ausgegeben werden.
    k = 100                                                                   #einfach eine große zahl, damit genügend viele Iterationen für T_i vorhanden sind.
    h = b-a                                                                   #a, b = untere und obere integralgrenzen. somit ist h der raum der x-achse über den integriert wird.
    T_i = []                                                                  #
    T_i.append( 0.5*h*(func(a)+func(b)) )                                     #T_1 laut definition (z.b: NumerikFürIngenieureUndNaturwissenschaftler S.349 Gl: 10.4). das sind quasi die äußersten eckpunkt des ersten trapezes.                                       #
    if ausgabe == 1:
        print(f"T_1    {T_i[0]:>15.6f}")
    for i in range(1,k):                                                      #
                                                                              #
        T_im = T_i[::]                                                        #copy von liste T_i wird erstellt. in T_im wird die "vorherige" zeile der romberg-matrix gespeichert.
                                                                 
        try:                                                                  #
            T_i[0] = T_im[0] / h                                              #wir teilen hier T_i[0] (T_im ist eine kopie von T_i) durch h, damit wir T_i[0] nicht jedesmal komplett neu berechnen müssen, ...
        except ZeroDivisionError as e:
            print("Fehler:", e)                                               #fängt Fehler ab, wenn man z.B von x = 5 bis 5 integrieren will.
            break
                                                                              #     ...sondern nur die neuen "stützpunkte", die sich zwischen den bereits vorhandenen Trapezen befinden, zur alten trapezsumme addieren müssen.
        h /= 2                                                                #h wird immer halbiert: von T_1 -> T_2; T_2 -> T_4; T_4 -> T_8 usw.
        
        step_size = 1
        for ii in range(2**(i-1)):        
            T_i[0] += func(a+h*step_size)                                     #neues T_i[0] wird berechnet. Die T_i[0] sind dabei die erste Spalte in der Romberg-Matrix und berechnen sich wie folgt: ... 
                                                                              #     ...T(h) = h*[0.5*f(a) + f(t_1) + ... + f(t_n-1) + 0.5*f(b)]
            step_size += 2                                                    #die zahl 2, weil: |1 x x x 5 x x x 9|   ---->   |1 x 3 x 5 x 7 x 9|   ---->   |1 2 3 4 5 6 7 8 9|, wobei "x" die noch fehlenden stützpunkte sind.
                                                                              #                  stepsize = 1; h=4            stepsize = 1,3; h=2            stepsize = 1,3,5; h = 1
                                                                              #                                               wobei die "5" "ausgelassen"
                                                                              #                                               wird, da sie schon in T_i[i-1]
                                                                              #                                               berechnet wurde.
        T_i[0] *= h                                                           #jetzt wird das h mit der richtigen summe multipliziert. richtige summe, weil die "stützstellen" jetzt eingefügt sind.
        
        T_i += [0]                                                            #hier wird die liste T_i um ein element erweitert, da im nächsten schritt ein neues T_i dazukommt.  
        for j in range(1, i+1):
            T_i[j] = (4**j*T_i[j-1]-T_im[j-1])/(4**j-1)                       #rekursionsschritt: aus T_i[i,j-1] und T_i[i-1, j-1] --> T_i[i,j] (z.b: NumerikFürIngenieureUndNaturwissenschaftler S.363 Abb: 10.3)  
                                                                              #schöne darstellung des endergebnisses mit T_1, T_2, T_4, usw. als Satzanfang.
        if ausgabe == 1:
            Trapez_T_i = 2**(len(T_i)-1) 
            for i in range(len(T_i)):
                if i == 0:
                    print(f"T_{Trapez_T_i:<5}", end = "")
                if i != len(T_i)-1:
                    print(f"{T_i[i]:>15.6f}", end = "")
                else:
                    print(f"{T_i[i]:>15.6f}")
        
        
        precision = abs(T_i[i]-T_im[i-1])                                                   #wenn die differenz der letzten beiden elemente der hauptdiagonale der romberg-matrix kleiner als epsilon (oben frei wählbar) sind,
        if (precision < epsilon):
            if ausgabe == 1:                                                                #     ...gilt das ergebnis der romberg funktion als genügend präzise.  
                print(f"Geschätztes Ergebnis durch Romberg nach {len(T_i)} Iterationen:")   #exaktes resultat des integrals: pi/2 + exp(pi/2) - 2 
            return T_i[i]
            
                     
print("Romberg Schema (Elemente auf 6 Nachkommastellen begrenzt):")  
print(f"{romberg(func_test, 0, math.pi/2, epsilon = 1e-4)}") 
print(f"Analytisches Ergebnis:\n{math.pi/2 + math.exp(math.pi/2) - 2}")

#Im anschließenden Teil soll noch qualitativ eine zweifache Integration der Erdbeschleunigung g durchgeführt werden,
#    ...um so die "parabelförmige Wurfkurve" (s = 0.5*g*t**2) zu zeigen. 

fig = plt.figure(figsize = (8,10))
grd = fig.add_gridspec(6,1)
drw = fig.add_subplot(grd[0:2,:])
drw.set_title("Zweifache Integration der Erdbeschleunigung \ng bzw. $F_{g}$ durch das Romberg-Schema", fontsize = 15)
time = np.arange(0, 10, 1)
drw.plot(time, [gravity(x) for x in time], 'b-')
drw.yaxis.set_label_coords(-0.15, 0.5)
drw.set_ylabel('force')

velocity = []
for i in range(len(time)-1):
    velocity_list = romberg(gravity, 0, time[i+1], ausgabe = 0)                #es wird jeweils von 0 bis zu einem bestimmten Zeitpunkt integriert.
    velocity.append(velocity_list)
    

drw = fig.add_subplot(grd[2:4,:])
drw.plot(time[:-1], velocity, 'r-')                                            #damit die dimensionen von xn und yn zusammenpassen (es ist immer eine stützstelle mehr benötigt als es datenpunkte zu berechnen gibt)
drw.yaxis.set_label_coords(-0.15, 0.5)
drw.set_ylabel('velocity')

def lagrange(x):                                                               #ein Lagrange Polynom interpoliert eine Liste von Werten im x,y-Koordinatensystem...
    xn = time[:-1]                                                             #    somit erhalten wir eine Funktion 'lagrange(x)', die kontinuierlich ist, ...
    yn = velocity                                                              #    und damit wieder in die romberg-Funktion eingespeist werden kann...
    ergebnis_sum = 0                                                           #    für die zweite Integration von F_g.
    for i in range(0,len(xn)):
        ergebnis_product = 1
        for j in range(0, len(xn)):
            if i == j:
                continue
            else:
                ergebnis_product = (x - xn[j])/(xn[i]-xn[j])*ergebnis_product
        ergebnis_product = yn[i] * ergebnis_product
        ergebnis_sum = ergebnis_product + ergebnis_sum
    return ergebnis_sum  


distance = []
for i in range(len(velocity)-1):
    distance.append(romberg(lagrange, 0, time[i+1], ausgabe = 0))     


drw = fig.add_subplot(grd[4:6,:])
drw.plot(time[:-2], distance, 'g-')
drw.set_ylabel('distance')
drw.set_xlabel('time') 
drw.yaxis.set_label_coords(-0.15, 0.5)

plt.tight_layout()
#plt.savefig("abschlussprojekt_trajektorien_.png")
plt.show                                                                      #die ausgegebenen Werte sind natürlich Quatsch und sind nur qualitativ, da nicht wirklich die konstante Funktion F_g integriert wurde.

    
    