# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 11:45:45 2021

@author: aleX glötzl
"""
import numpy as np

zeilen_laenge = 55
path = r"C:\Users\aleX\Kurse\Algo_u_Daten\exam\gg7.txt"
path_test = r"C:\Users\aleX\Kurse\Algo_u_Daten\exam\gg7_test.txt"
path_good = r"C:\Users\aleX\Kurse\Algo_u_Daten\exam\gg7_good.txt"
path_naive = r"C:\Users\aleX\Kurse\Algo_u_Daten\exam\gg7_naive.txt"

with open(path, "r") as handle:
    text = handle.read().splitlines()
    #text = handle.readlines()
    #text = handle.read()

alle_woerter = []
for line in text:
    line_woerter = line.split(" ")
    for wort in line_woerter:
        if len(wort) != 0:                                                      # exception for a space behind "7" in line 2. line.split("") (without the space) did not work
            alle_woerter.append(wort)
            
#print(alle_woerter)
    
#===========================# Good raggedright #==========================================#

def dynamic(woerter, width):

    anzahl = len(woerter)
    #print("Anzahl Wörter: ", anzahl)
    kum_len = [[0] * anzahl for i in range(anzahl)]
    for i in range(anzahl):
        kum_len[i][i] = width - len(woerter[i])                                 # worst case: jede zeile hat nur ein wort. 
                                                                                # also kann in der zweiten zeile selbst im schlechtesten fall erst das zweite wort stehen. 
                                                                                # also können wir das erste wort in zeile 2 (=kum_len[1][0]) ignorieren.
        for j in range(i + 1, anzahl):
            kum_len[i][j] = kum_len[i][j - 1] - len(woerter[j]) - 1             # letztes '-1' wegen leerzeichen
            if kum_len[i][j] < 0:
                kum_len[i][j] = np.inf                                          # ist das zeilenende errreicht, können wir diese worte/werte ebenfalls ignorieren
    '''
    print("kumulierte Längen der Wörter pro Zeile")                             # beispiel für das dritte element von kum_len:
    for i in range(len(kum_len)):                                               # [ 0.  0. 52. 37. 25. 21. 19. 15. 11.  3. inf inf ... ]
        kum_len_arr = np.array(kum_len)                                         # dritte zeile, daher ersten beiden elemente der liste leer.
        for ii in range(len(kum_len_arr[i])):                                   # 55- len("die") = 52
            kum_len_arr[i][ii] = str(kum_len_arr[i][ii]).zfill(2)               # 52- len("Bundesrepublik") -1 = 37
        print("kumLen"+str(i).zfill(2)+": ",kum_len_arr[i])                     # 37 - len("Deutschland") -1 = 25
    '''                                                                         # kum_len gibt also die anzahl an vorhandenen leerzeichen abhängig 
                                                                                # von der zeile und den bisher eingesetzten wörtern an.

    memory_ij = [[0, 0] for i in range(anzahl)]                     
    strafe = [0] + [np.inf] * anzahl                                            # die strafe "vor" der ersten zeile ist null, da die erste zeile der anfang des textes ist.
                                                                                # daher strafe[0] = 0. strafe[j] ist die minimale strafe aller bisherigen worte einschließlich des j-ten wortes.
    
    for j in range(anzahl):                                                     # die beiden loops schauen in kum_len[i][j] nach einer neuen minimalen strafe für das j-te wort.
                                                                                # beispiel: j = 5, (i = 2): kum_len[2][5] = strafe[2] + kum_len[2][5] **2, d.h.
                                                                                # zwei wörter sind bereits innerhalb der ersten zwei zeilen untergebracht mit der ges. strafe                                                                 
                                                                                # strafe[2] und die wörter mit index i=2,3,4,5 sind bei kum_len[2][5] in der dritten zeile unter-
                                                                                # gebracht. es wird über i iteriert und die minimalste strafe wird in strafe[6] gespeichert.
        for i in range(j+1):
            if kum_len[i][j] == np.inf:                                         # wie schon erwähnt werden diese worte ignoriert, weil sie über den zeilenrand stünden.
                temp_strafe = np.inf
            else:
                temp_strafe = strafe[i] + kum_len[i][j] ** 2
            if strafe[j + 1] > temp_strafe:
                strafe[j + 1] = temp_strafe

                memory_ij[j] = [i, j]                                           # memory_ij[7] = [4,7], d.h. die acht worte (j=7) sind aufgeteilt in: 4 in ersten 4 zeilen und 4 in der 5. zeile.
                #print(i, j)                                                    # das ist in sofern nützlich, da das letzte element der fertigen liste memory_ij die minimalste strafe
                                                                                # des gesamten textes ausgibt, in unserem beispiel wäre das letzte element des ges. textes [196, 201].
                                                                                # es gibt 202 wörter und für die minimalste strafe wurde die strafe[196] (=1119) für die vorletzte zeile gewählt.
                                                                                # also sind 6 wörter in der letzten zeile. von da aus kann man sich dann mit hilfe der strafen[i] 
                                                                                # "zurückhangeln" und die line breaks bestimmen.
    # print(memory_ij)                                                            
    # print()
    # print("minimale Strafe: ",strafe)
    # print()
    # print("Memory_ij: ",memory_ij)                

    line_break = [0]*anzahl
    j = anzahl
    while j > 0:                                                                # angesprochenes "zurückhangeln" wobei nach und nach die letzte zeile entfernt wird und
        i = memory_ij[j-1][0]                                                   # die jeweiligen line breaks gespeichert werden.
        line_break[j-1] = 1
        j = i 
        
    strafe_ohne_ltzt_zeile = strafe[memory_ij[-1][0]]                           # strafe[196] (=1119) ist die strafe aller worte einschließlich der vorletzten zeile
                                                                                # und somit der gesuchte special case, wo die strafe der letzten zeile ignoriert wird.
    #print(strafe_ohne_ltzt_zeile)
        
    #print(line_break)    
    with open(path_good, "w") as handle_out:
        for i, wort in enumerate(woerter):
            if line_break[i] == 0:
                handle_out.write(wort+" ")
            else:
                handle_out.write(wort+line_break[i]*"\n")    
        handle_out.write("\n\nStrafe: "+str(strafe_ohne_ltzt_zeile))

    return
            
dynamic(alle_woerter, zeilen_laenge) 

     
#===========================# Naive justified #==========================================#
# Da ich den naiven ansatz zuerst geschrieben habe, habe ich ihn hier der vollständigkeit eingefügt.  
# Mir ist klar, dass danach nicht gefragt war.

def naive_justified(woerter, width):
    woerter_anzahl = len(woerter)         
    #print(woerter_anzahl, woerterr)
    
    woerter_laenge = []
    for wort in woerter:
        laenge = len(wort)
        if laenge != 0:
            woerter_laenge.append(laenge)
        
    #print(woerter_laenge)
    line_break = [0 for i in range(woerter_anzahl)]
    
    maxi_woerter = 0                                                            #temporärer speicher, um die maximalen buchstaben/wörter pro zeile zu bestimmen
    maxi_woerter_list = []                                                      #maximale buchstaben/wörter pro zeile
    for i, laenge_i in enumerate(woerter_laenge):
        #print("anfang:", i, laenge_i)
        if maxi_woerter+laenge_i < zeilen_laenge:                               # CASE 1: das wort passt in die zeile rein (+ mind. ein weiteres leerzeichen platz)
            
            #print("case 1:", maxi_woerter+laenge_i)
            maxi_woerter += (laenge_i+1)                                        # '+1' wegen leerzeichen 
            #print(maxi_woerter)
            
        elif maxi_woerter+laenge_i == zeilen_laenge:                            # CASE 2: das wort passt gerade noch so in die zeile ohne leerzeichen dahinter
            #print("case 2:", maxi_woerter+laenge_i)
            line_break[i] = 1
            maxi_woerter_list.append(maxi_woerter+laenge_i)
            maxi_woerter = 0 
            
        else:                                                                   # CASE 3: wort passt nicht mehr in die zeile
            #print("case 3:", maxi_woerter+laenge_i)
            line_break[i-1] = 1
            maxi_woerter_list.append(maxi_woerter-1)
            maxi_woerter = laenge_i+1
            #print(maxi_woerter)
        
        
    #print(line_break)  
    maxi_woerter_list_array = np.array(maxi_woerter_list)
    leerzeichen_pro_zeile = zeilen_laenge - maxi_woerter_list_array
    strafe_naive = np.sum(leerzeichen_pro_zeile**2)
    #print(strafe_naive)
    #print(maxi_woerter_list)  
    #print(leerzeichen_pro_zeile)
    
    with open(path_naive, "w") as handle_out:
        for i, wort in enumerate(alle_woerter):
            if line_break[i] == 0:
                handle_out.write(wort+" ")
            else:
                handle_out.write(wort+line_break[i]*"\n")
        handle_out.write("\n\nStrafe: "+str(strafe_naive))    

    return
    
naive_justified(alle_woerter, zeilen_laenge) 
#print(len(alle_woerter))    
