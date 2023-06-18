# -*- coding: utf-8 -*-
"""
Created on Thu May  5 21:30:58 2022

@author: aleX
"""
import tazCentroids as tC
import os
import re
import numpy as np
import pandas as pd

alphabet = "abcdefghijklmnopqrstuvwxyzäöüß"

def predict_selection(textfile: str, letterfreq_centroids: list, letters: str) -> int:
    '''
    Parameters
    ----------
    textfile : str
        path to undefined file
    letterfreq_centroids : list
        list of two lists each containing the relative letter frequencies of both
        centroids. first element corresponds to 2015, second to 2018.
    letters : str
        which letters to compare

    Returns
    -------
    TYPE : int
        prediction of the year:
        2015
        2018 (also for equal distance)
    '''
    lett_text = np.array(tC.countFrequencies(textfile))
    
    lett_cent = np.array(letterfreq_centroids)
    
    # centroid1 = letterfreq_centroids[0]
    # centroid2 = letterfreq_centroids[1]
    
    index_mask = [alphabet.index(letter) for letter in letters]
    #print(index_mask)
    #print(lett_text, lett_cent)
    
    distance1 = np.sqrt(sum((lett_cent[0,index_mask]-lett_text[index_mask])**2))
    distance2 = np.sqrt(sum((lett_cent[1,index_mask]-lett_text[index_mask])**2))
    
    #print(distance1, distance2)
    if distance1 < distance2:
        return 2015
    else:
        return 2018 #also contains case for equal distance to both centroids but very unlikely

def evaluate_classifier(testfiles: str, targets: list, letterfreq_centroids: list, letters: str, cross_table=False):
    '''
    Parameters
    ----------
    testfiles : str
        list of paths of undefined files to predict
    targets : list
        true classification of test files, i.e [2015,2015,2018,...]
    letterfreq_centroids : list
        list of two lists each containing the relative letter frequencies of both
        centroids. first element corresponds to 2015, second to 2018.
    letters : str
        which letters to compare
    cross_table: boolean
        prints out a cross table of predicted vs. real year
        
    Returns
        incorrectly guessed texts;
        made predictions on texts
    None.
    '''
    predictions = []
    for i in range(len(testfiles)):
        
        temp_pred = predict_selection(testfiles[i], letterfreq_centroids, letters)
        predictions.append(temp_pred)
    
    #print(predictions)
    predictions = np.array(predictions)
    targets = np.array(targets)
    incorrect = sum(predictions != targets)
    
    if cross_table:
        print("Cross Table:")
        my_table = pd.crosstab(predictions, targets, rownames=["pred"], colnames=["true"])
        print(my_table,"\n")
        
    return incorrect, predictions
    
    


if __name__ == "__main__":
    #in den ordner tazTexts wurden die vorherigen texte eingefügt.  
    #ordnerstruktur:
    #    *blatt2.py
    #    *moreTazTexts
    #        *tazTexts
    #           *Leibesuebungen
    #           *tazTexts
    #           *TestTexts
    #           *Wirtschaft und Umwelt
    #        *UnidentifiedTexts

    #used same code as last week for importing files
    path = r".\moreTazTexts"
    
    txt_files = []
    for dirpath, dirnames, filenames in os.walk(path): #path+r"\TestTexts"
        for name in filenames:
            if name[-3:] == "txt":
                txt_files.append(os.path.join(dirpath, name))
            
    # print(txt_files, "\n")
    # print(len(txt_files))
    
    pattern = re.compile("_2015_")
    pattern2 = re.compile("_2018_")
  
    list_2015 = []
    list_2018 = []
    list_unidentified = []
    
    for file in txt_files:
        result = re.findall(pattern, file)
        result2 = re.findall(pattern2, file)
        if result:
            list_2015.append(file)
        elif result2:
            list_2018.append(file)
        else:
            list_unidentified.append(file)
           
    
    #I added "encoding='utf8' "to the sample solution when trying to read the file, otherwise it does not work on my computer
    freq_2015, centroid_2015 = tC.computeCentroid(list_2015)
    freq_2018, centroid_2018 = tC.computeCentroid(list_2018)
    

    my_targets =  [2015 for i in range(len(list_2015))] + \
                    [2018 for i in range(len(list_2018))]
    incorrect, my_predictions = evaluate_classifier(list_2015+list_2018, my_targets, [centroid_2015, centroid_2018], "ae", cross_table=True)
    
    print("prediction on test set:")
    print("incorrectly guessed: ",incorrect)
    #true positive: 29
    #true negative: 12
    #false negative:41
    #false positive:14
    #precision = 29 / (29 + 14) = 0.674
    #recall = 29 / (29 + 41) = 0.414
    #f1-score = 2*0.674*0.414 / (0.674+0.414) = 0.513
    
    
    classifiers = ["mi", "ms", "ei"]
    best_classifier = []
    for letter in classifiers:

        incorrectly, _ = evaluate_classifier(list_2015+list_2018, my_targets, [centroid_2015, centroid_2018], letter, cross_table=False)
        best_classifier.append(incorrectly)
    
    
    best_index = np.argmin(best_classifier)
    print("best classifier 2-letters are:", classifiers[best_index], "with incorrect guesses:", best_classifier[best_index])
    worst_index = np.argmax(best_classifier)
    print("worst classifier 2-letters are:", classifiers[worst_index], "with incorrect guesses:", best_classifier[worst_index])    
    
    
    
    classifiers2 = ["msi", "mse", "mei", "sei"] #"bil", "ilr", "mie", "msi"
    best_classifier2 = []
    for letter in classifiers2:

        incorrectly, _ = evaluate_classifier(list_2015+list_2018, my_targets, [centroid_2015, centroid_2018], letter, cross_table=False)
        best_classifier2.append(incorrectly)
    
    
    print()
    best_index2 = np.argmin(best_classifier2)
    print("best classifier 3-letters are:", classifiers2[best_index2], "with incorrect guesses:", best_classifier2[best_index2])
    worst_index2 = np.argmax(best_classifier2)
    print("worst classifier 3-letters are:", classifiers2[worst_index2], "with incorrect guesses:", best_classifier2[worst_index2])    
    print("\n=> using 3 letters does not improve accuracy.")
    
    
    print("\nbegin of exercise D.4")
    # path2 = path+r"\UnidentifiedTexts"       
    # undefined_files = [os.path.join(path2,file) for file in os.listdir(path2)] #os.path.join(path,file)
    
    #print(classifiers[best_index])
    my_predictions_unknownfiles = []
    for file in list_unidentified:
        my_temp = predict_selection(file, [centroid_2015, centroid_2018], classifiers[best_index])
        my_predictions_unknownfiles.append(my_temp)


    print()
    print("actual published years according to google:")
    print("[2018, 2015, 2018]")
    print("predicted:")
    print(my_predictions_unknownfiles)    
    

    
    #An attempt to find a better classifier by biggest difference in letter frequency:
    total_diff = abs(np.array(centroid_2015)-np.array(centroid_2018))
    #print(total_diff, len(total_diff))
    
    #the index of the 2 letters with biggest relative freq. difference are:
    best_letters_ind = np.argsort(total_diff)[-2:]
    #print(best_letters_ind)
    #print(total_diff[best_letters_ind])
    
    classifier3 = [alphabet[c] for c in best_letters_ind]
    classifier3 = "".join(classifier3)
    print("best letters for differentiation:", classifier3)
    
    my_predictions_unknownfiles = []
    for file in list_unidentified:
        my_temp = predict_selection(file, [centroid_2015, centroid_2018], classifier3)
        my_predictions_unknownfiles.append(my_temp)
    
    
    print()
    print("after the attempt to find more suitable classifiers:")
    print("actual published years according to google:")
    print("[2018, 2015, 2018]")
    print("predicted with max diff as classifier:")
    print(my_predictions_unknownfiles) 
    
    
    
    
    
    
    
    