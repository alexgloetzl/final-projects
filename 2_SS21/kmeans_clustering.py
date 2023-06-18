# -*- coding: utf-8 -*-
# ============================================================================ #
# Python für Fortgeschrittene - Wissenschaftliche Anwendungen
# Final Project - KMeans clustering
# Summer Term 2021
# 
# Name
#     Alexander Glötzl, Mat.Nr. 1627077, benotet
# ============================================================================ #


#%matplotlib qt
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import pandas as pd
from os.path import join
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import sys

#kurz ein, zwei worte: der eigentlich algorithmus ist von zeile 64 bis 127. Um die daten auch entsprechend visuell darstellen zu können
#wurden für 2D und 3D noch entsprechende scatter plots erstellt. außerdem wurde für jede anzahl an clustern eine art "score" berechnet.
#in der literatur nennt man diesen inertia score. dieser entspricht der summe der quadrierten distanz zwischen jedem datenpunkt und seinem dazu-
#gehörigem centroiden. somit kann am ende der benutzer die "optimale" anzal an centroiden für seine daten visuell anhand einer grafik auswählen.
#will man's noch genauer wissen, müsste der silhouette score für jeden datenpunkt berechnet werden.

pd.set_option('display.max_columns', 500)                                       #damit bei print(dataframe) auch alle spalten ungekürzt angezeigt werden
#random.seed(98)

def kmeans(dataframe: pd.DataFrame, k_start: int = 2, k_end: int = 10) -> None:    
    dataframe.dropna(axis=0, inplace=True)                                      #wenn ein feature eines landes fehlt, soll die komplette zeile entfernt werden

    df_names = pd.Series(dataframe.index)
    X_non_scaled = dataframe.values   

    scaler = StandardScaler()                                                   #wir benutzen einen scaler, damit features mit großen zahlen nicht deutlich mehr ins gewicht fallen, als features mit kleinen zahlen bei der berechnung von distanzen.
    scaler.fit(X_non_scaled)
    X = scaler.transform(X_non_scaled)    
    
    iterations = 100                                                            #die anzahl an iterationen, die der algorithmus hat die koordinaten der centroiden zu finden. es kann auch schon vorher fertig sein.
    best_out_of_iterations = 10                                                 #für jedes k an clustern werden 10 score/ inertia werte berechnet und der beste/minimalste davon wird genommen. beim minimalsten wert ist davon auszugehen,
                                                                                #dass der richtige centroid für das jeweilige cluster gefunden wurde.
    
    k_clusters_list = []                                                        #liste, in der meine inertia werte der daten für k cluster gespeichert werden.
    kmeans_inertia = []                                                         #liste, in der die inertia werte von kmeans (sklearn.cluster.KMeans) gespeichert werden.
    labels_dict = {}
    
    if k_end < k_start:
        raise ValueError("Start of cluster range must be smaller or equal than end of cluster range.")
        
    elif X.shape[1] < 2:
        raise ValueError("There need to be at least 2 features selected for each country.")
    
    for k in range(k_start,k_end+1):
    
        print(f"labeling data for {k} clusters")
        
        kmeans = KMeans(n_clusters=k)                                           
        kmeans.fit(X)
        kmeans.predict(X)
        kmeans_inertia.append(kmeans.inertia_)                                                  #"professioneller" inertia wert
        
        total_score_dict = {}
    
        for n_iter_best in range(best_out_of_iterations):                                       #ich lasse für jede anzahl an clustern mehrere loops durchlaufen und nehme den besten bzw. minimalsten "distance-score"
            rand_centroid_index = random.sample(range(X.shape[0]),k)
    
            new_centroids = X[rand_centroid_index]
                
            labels = np.zeros(X.shape[0])
    
            for n_iter in range(iterations):                                                    #dieser loop berechnet die neuen labels, updated daraufhin die centroiden (zentren der cluster) wiederholt diese beiden schritte bis sich die position der centroiden nicht mehr ändert. 
    
                old_centroids = new_centroids
                distances = np.zeros((X.shape[0], k))
                for k1 in range(k):
    
                    for n in range(X.shape[0]):
                        temp_dist_to_k_cluster = 0
                        for i in range(X.shape[1]):
                            temp_dist_to_k_cluster += (X[n, i] - new_centroids[k1, i])**2       #euklidische distanz
    
                        distances[n, k1] = math.sqrt(temp_dist_to_k_cluster)                    #in der ersten spalte von distances befindet sich die distanz jedes datenpunktes zu dem ersten centroiden. für die zweite spalte usw. ...
    
                
                labels = np.argmin(distances, axis = 1)                                         #die kleinste distanz zum jeweiligen centroiden bestimmt zu welchem centroiden dieser datenpunkt gehört
                myValues, myCounts = np.unique(labels, return_counts=True)                      #returns list automatically sorted
                if len(myValues) != k:
                    #print("hoppla!")
                    break                                                                       #für den seltenen fall, dass bei der iteration ein centroid entsteht, der komplett leer ist, d.h. dass z.B. keine instanz zum cluster 3 gehört, wurde hier eine ausnahme einführt.
                                                                                                #Für random.seed(98) ist für k = 9 cluster (also 10 cluster) das für n_iter_best = 0 beispielsweise der fall. das führt dazu, dass aufgrund der Nan-werte die mittelwerte nicht mehr
                                                                                                #richtig gebildet werden können. ich weiß, es gibt np.nanmean, aber ich fand es sinnvoller für diesen seltenen fall (wkt. ungefähr: 1/1000, weil random.seed(0...99) & n_iter_best(0...9))      
                                                                                                #einfach eine ausnahme einzuführen.
                
                
                new_centroids = np.zeros((k, X.shape[1]))

                for k2 in range(k):
                    myMask = labels == k2
                    new_centroids[k2, :] = np.mean(X[myMask, :], axis = 0)                      #mittelwert wird über alle datenpunkte gebildet für den neuen centroiden mit dem selben label wie die datenpunkte
                # if k == 9 and n_iter_best == 0 and n_iter < 10:
                #     X_rescaled = scaler.inverse_transform(new_centroids)
                #     print(X_rescaled)
                if ((new_centroids == old_centroids).all()):                                    #old == new ist die abbruchbedingung für den algorithmus
                    
                    total_score = 0                                                             #am ende des algorithmus wird der score/inertia wert berechnet
                    for k3 in range(k):
                        score = 0
                        for i in range(X.shape[0]):
                            if labels[i]==k3:
                                score += (distances[i, labels[i]])**2                           #"inertia is the squared distance between each instance and its closest centroid"
                        
                        total_score += score         
                    
                    if total_score not in total_score_dict:                                     #hier werden die inertia werte gesammelt, um am ende den besten auszuwählen
                       total_score_dict[total_score] = [new_centroids, labels] 
                    
                    break
    
        best_centroids_key = min(total_score_dict)                                              #bester key/inertia wert wird für jedes k clustern ausgewählt und gespeichert
        k_clusters_list.append(best_centroids_key) 
        
        best_centroids = total_score_dict[best_centroids_key][0]
        best_centroids_labels = total_score_dict[best_centroids_key][1]   
        labels_dict[k] = best_centroids_labels                                                  #wir brauchen die labels, um später die namen der länder richtig zu gruppieren zu können.
        
        X_rescaled = scaler.inverse_transform(X)                                                #daten werden wieder zurücktransformiert
        best_centroids_rescaled = scaler.inverse_transform(best_centroids)  
        
        
        if X.shape[1] == 3:                                                                     #3D scatter plot für exakt 3 features
            fig, ax = plt.subplots(1, 1, dpi=300)                                               #leider funktioniert zorder für 3D nicht richtig und die centroiden sind teilweise nur schlecht sichtbar unter den anderen datenpunkten
            ax = plt.axes(projection ="3d")

            myScatter = ax.scatter3D(X_rescaled[:,0], X_rescaled[:,1], X_rescaled[:,2], c=best_centroids_labels, label=k, zorder=-1, alpha=0.5)
            
            ax.set_xlabel(dataframe.columns[0])
            ax.set_ylabel(dataframe.columns[1])
            ax.set_zlabel(dataframe.columns[2])
        
            ax.legend(handles=myScatter.legend_elements()[0], labels=range(1,k+1), prop={'size': 6}, loc="best")#,title="clusters"
            ax.scatter3D(best_centroids_rescaled[:,0], best_centroids_rescaled[:,1], best_centroids_rescaled[:,2], c=np.unique(best_centroids_labels), marker="*", s=60, zorder=1, alpha=1, edgecolors='k')
       
        elif X.shape[1] == 2:                                                                   #2D scatter plot
            fig, ax = plt.subplots(1, 1, dpi=300)

            myScatter = ax.scatter(X_rescaled[:,0], X_rescaled[:,1], c=best_centroids_labels, label=k, zorder=-1, alpha=0.5)
            ax.set_xlabel(dataframe.columns[0])
            ax.set_ylabel(dataframe.columns[1])
        
            ax.legend(handles=myScatter.legend_elements()[0], labels=range(1,k+1), prop={'size': 6}, loc="best")#,title="clusters"
            
            ax.scatter(best_centroids_rescaled[:,0], best_centroids_rescaled[:,1], c=np.unique(best_centroids_labels), marker="*", s=60, zorder=1, alpha=1, edgecolors='k')
          
        else:
            continue
    
    #print(kmeans_inertia)
    #print(k_clusters_list)
    fig, axs = plt.subplots(2,1, sharey= True, sharex = True, dpi=300)
    axs[0].plot(range(k_start,k_end+1), k_clusters_list)
    axs[1].plot(range(k_start,k_end+1), kmeans_inertia)
    axs[0].title.set_text("Score of minimal distances of each instance to its centroid.\nSmaller is better. Look for the steepest fall for optimal number of clusters.")
    axs[1].set_xlabel("number of clusters")
    axs[0].set_ylabel("my score/inertia")
    axs[1].set_ylabel("inertia from kmeans")

    plt.tight_layout()
    plt.show()
    
    while 1:                                                                    #hier kann der benutzer die "optimale" anzahl an centroiden auswählen anhand des oben erzeugten bildes (meistens ist dieser bei k = 3 oder 4) 
        print("Choose how many clusters do you want?")                          #je mehr centroiden, desto kleiner wird natürlich auch der score. es geht hier darum das k mit dem ersten "steilsten" fall des scores für ein optimales ergebnis zu nehmen.
        print(f"You can choose from: {list(range(k_start,k_end+1))}")
        input_k = input(">>:")
        try:
            #input_k =int(input(">>:"))
            input_k = int(input_k)
            if input_k not in list(range(k_start,k_end+1)):                     #fehler abfangen, z.B input "10" bei range [2, 3, 4, 5]
                print("Please enter a number in the correct range.")
                print()
                continue
            else:
                break

        except:                                                                 #falls man vorzeitig das programm beenden möchte. ctrl+c funktioniert an dieser stelle nämlich nicht mehr.
            if input_k == "quit":
                sys.exit('quitting...')
            #raise TypeError(f"Fehlerhafte Eingabe. Bitte eine Zahl aus der Liste {list(range(k_start,k_end+1))} eingeben.")
            print("Incorrect input!")                                           #fehler abfangen: alles input keine zahl ist, z.B. string
            print()
    
        
    labels = labels_dict[input_k]
    myValues, myCounts = np.unique(labels, return_counts=True)  
    for i in range(len(myValues)):
        print(f"{i+1} out of {input_k} clusters: {myCounts[i]} out of {len(labels)} countries:")        #zusätzliche informationen zu den clustern: anzahl an ländern, name der länder, koordinaten der centroiden/ mittelwerte
        print(df_names[labels==i].to_list())#to_string(index=False)
        print("<< Mean values of clusters/ centroid coordinates: >>")
        new_df = pd.DataFrame(best_centroids_rescaled, columns=dataframe.columns)
        print(new_df.iloc[[i]].to_string(index=False))
        print()
    
    
    while 1:
        print("Type in your desired country, which you want to know more about.\nFor example: germany, united states, togo.")
        country = input(">>:")
        country_case_insensitive = "(?i)"+country                                                       #(?i) für case insensitivity. also nicht nur Germany, sondern auch germany möglich
        country_name = df_names[df_names.str.match(pat = country_case_insensitive)].values
        
        if country_name.size == 0:# or country_name not in df_names.values:                             #fehler abfangen (z.B "ger many oder zahlen")
            print("This country doesn't exist or the database is incomplete for the selected features (GDP, Population, ...).")    
            print()
        else:
            break
    

    country_label_index = labels[df_names.str.match(pat = country_case_insensitive)][0]                 #zusätzliche informationen zu einem bestimmten land, z.B united states
    country_name_index = df_names[df_names.str.match(pat = country_case_insensitive)].index[0]
    print(f"{country} is in cluster {country_label_index+1} out of {input_k} with following statistics:")
    print("")
    print(f"{df.loc[df_names[country_name_index], :]}")
    
    return



fact_root = r"C:\Users\aleX\Kurse\Python\python_kurs_fortge\Blatt6\factbook.csv-master"                 #factbook wurde wie in den übungen als datenquelle verwendet

categories = pd.read_csv(join(fact_root, "categories.csv"))

relevantCategories = [                                                                                  
    "GDP (purchasing power parity)",                                                                    #hier werden per hand die gewünschten daten eingetragen
    "Life expectancy at birth"#,                                                                        #will man die 2d scatter plots sehen, muss man 2 datensätze/features laden.                                  
    #"Population",                                                                                      #für 3D braucht man 3 features.     
    #"Public debt"                                                                                      #für mehr als 3 features ist keine visualisierung vorhanden. nur die einordnung per konsolen text
]

filenames = {
    category: f"c{int(categories.Num[categories.Name == category])}.csv"
    for category in relevantCategories}

sources = {
    category: pd.read_csv(join(fact_root, "data", filename), sep=',') for category, filename in filenames.items()
}

for key in sources:
    sources[key].drop("Pos", axis="columns", inplace=True)
    sources[key].set_index("Name", inplace=True)
    sources[key].columns = [key]
    
# bei GDP ist die einheit "$" in der spalte. mit der folgenden zeile, wird dies behoben
sources["GDP (purchasing power parity)"]["GDP (purchasing power parity)"] = sources["GDP (purchasing power parity)"]["GDP (purchasing power parity)"].str.replace(r'\D', '')

df = pd.concat(sources.values(), axis=1)    
                                                    

kmeans(df, k_start = 2, k_end = 10)
#kmeans(df)

 


