# -*- coding: utf-8 -*-
# author: gloetzl aleX

#_______ A, _______

#1, 
# Beide definitionen erwähnen, dass gene aus dna bestehen und deshalb ein erbgut sind.
# Definition 1. erwähnt die translation von genen (mRNA -> Aminosäuresequenz -> proteine).
# Definition 2. erwähnt die transkription (mRNA aus DNA).
# Die Definitionen sind ähnlich aber definitiv nicht gleich/equivalent.

# #2,
# splicing: dna ->(transkription)-> pre-mRNA(enthält noch introns&exons) ->(splicing)-> 
# mRNA ->(translation)-> Aminosäuren -> proteine 
# exonen sind die teile/abschnitte des genes, die nach dem splicing noch erhalten sind
# introns sind die teile des genes, die nicht erhalten bleiben (splicing region).
# promoter regionen sind ein teil des genes, an die RNA polymerase andocken kann, um so mit die transkription zu beginnen zu können.
# untranslated regionen sind ein teil des genes, die zwar transkripiert aber nicht translatiert werden.

# #3,
# transkripte sind die abfolge der nukleotide, die die RNA ausmachen (nachdem diese durch transkription erzeugt wurde)
# die vier basen (auch nukleotide genannt) der RNA sind: Adenine, uracil, guanine, cytosine
# Exonen sind die orangenen rechtecke. Die dünnen linien sind die intronen.
# Für MMP3-201 gibt es 10 exonen.
# die länge der intronen habe ich nicht gefunden, aber man könnte sie theoretisch ausrechnen: 
#     length intron = transcript length 1,822 bps of whole gene minus bps of each exon
# Die "untranslated regions" könnten die non-protein coding blau farblich markierten stellen sein.

#_______ C, Part 1 _______

import random
import string

#print(string.ascii_lowercase)
random.seed(3)

N = 1000
myList = [random.choices(string.ascii_lowercase, k=N) for i in range(N)]

myList2 = [''.join(i) for i in myList]

#print(myList2)

matching_words = ["ali", "ada", "mark", "alex", "alexander"]
###matching_words_counter = [0 for i in matching_words]
match_dict = {matches : 0 for matches in matching_words}

for text in myList2:
    for i, char in enumerate(text):
        #print(i, end=" ")
        for match in matching_words:
            if text[i:(i+len(match))] == match:
                match_dict[match] += 1

print()
print(match_dict, end="\n\n")
# %%
#_______ C, Part 2 _______

import random
import string
import numpy as np

searched_word = "ali"
N = N_new = 2000
count = 0

#number of texts searched per iteration:
N_texts = 100

#so while-loop breaks if count > 50.
while 2*count < N_texts:
    count = 0
    N = N_new 
    
    #'only' 100 texts are searched per iteration (since not explicitly stated in exercise i think?). length of these texts will increase with N
    myList = [random.choices(string.ascii_lowercase, k=N) for i in range(N_texts)] 
    myList2 = [''.join(i) for i in myList]
    for text in myList2:
        for i, char in enumerate(text):
            #print(i, end=" ")
            if text[i:(i+3)] == searched_word:
                count += 1
                break #one match per text is enough -> break
    print("iter:", N, "counts:", count)          
    N_new += 1000
    
print("final:\niter:", N, "; min. counts:", count, "/", N_texts)


#now we rerun with our final N to find min, max and avg:
count_k = [0 for k in range(10)]
for k in range(10):
    myList = [random.choices(string.ascii_lowercase, k=N) for i in range(N_texts)] 
    myList2 = [''.join(i) for i in myList]
    for text in myList2:
        for i, char in enumerate(text):
            #print(i, end=" ")
            if text[i:(i+3)] == searched_word:
                count_k[k] += 1
    count_k_array = np.array(count_k)
    #average of counts of word "ali" over the N_texts=100 iterations for each k
    count_k_average = count_k_array/100

print(count_k_average)
min_count = min(count_k_average)
max_count = max(count_k_average)
avg_count = np.mean(count_k_average)

print("\nmin: ", min_count, "\nmax: ", max_count, "\navg: ", avg_count)
#der berechnete durchscnitt, gemittelt über 10 durchgänge, liegt höher als für 
#das final ermittelte N, da wir dort abgebrochen haben, 
#wenn minimal ein treffer für einen text dabei war. 
#es sind aber wahrscheinlich mehr als ein treffer pro text.

#also sollte das berechnete minimum größer gleich 0.5 sein
#und der berechnete durchschnitt über "count/N_texts" liegen,
#was sich mit dem berechneten ergebnis deckt:
# count/N_texts = 57 / 100
    
# min:  0.62 
# max:  0.85 
# avg:  0.753    

# %%
#_______ D _______
import os
import re
import string
import numpy as np
import matplotlib.pyplot as plt

path = r"C:\Users\aleX\Kurse\genomikII\week1\tazTexts"
#letters = string.ascii_lowercase

#walk through tazTexts to find all files present
txt_files = []
for dirpath, dirnames, filenames in os.walk(path):
    for name in filenames:
        if name[-3:] == "txt":
            txt_files.append(os.path.join(dirpath, name))
        

# print(txt_files)
# print(len(txt_files))

pattern = re.compile("_2015_")
pattern2 = re.compile("_2018_")

#result = re.search(pattern, "Umwelt_taz_2015_03_18.txt")
#result = re.findall(pattern2, "Umwelt_taz_2015_03_18.txt")

list_2015 = []
list_2018 = []

#group into two groups, namely 2015 and 2018, with the help of regex.
for file in txt_files:
    result = re.findall(pattern, file)
    result2 = re.findall(pattern2, file)
    if result:
        list_2015.append(file)
    elif result2:
        list_2018.append(file)
    else:
        print("i do not fit anywhere")

#print(list_2015, len(list_2015))
#print()
#print(list_2018, len(list_2018))
        
def count_frequencies(filepath: str) -> np.ndarray:
    
    with open(filepath, "r", encoding="utf8") as handle: #utf8 encoding important, otherwise non-latin letters cause problems
        line = handle.read().replace("\n", "")
        line = re.sub(r'[^\x00-\x7f]',r'', line) #yeet out all non-latin characters
        line_lower = line.lower()
        # print()
        # print(filepath)
        # print(line_lower)
     
    letters = string.ascii_lowercase
    letter_count_absolute = {i : 0 for i in letters}
    for char in line_lower:
        for c in letters:
            if char == c:
                letter_count_absolute[c] += 1
    
    #print(letter_count_absolute)
    
    #cannot make calculations on dictonary
    letter_count_relative = np.array(list(letter_count_absolute.values()))/sum(np.array(list(letter_count_absolute.values())))
    letter_count_relative = np.round(letter_count_relative, 5)
    
    #convert back to dict (was not asked for)
    letter_count_relative_dict = dict(zip(letters, letter_count_relative))
    #print(letter_count_relative)
    
    return letter_count_relative
    
#COMMENT OUT TO RUN FUNCTION
# filepath = list_2015[0]
# rel = count_frequencies(filepath)
# print(rel, sum(rel))


def compute_centroid(text_list: list):
    rel_freq_matrix = np.array([]).reshape(0,26)
    for text in text_list:
        rel_freq = count_frequencies(text)
        rel_freq_matrix = np.vstack((rel_freq_matrix, rel_freq)) #concatenate(, axis=0) didnt work with empty array
        
    #print(rel_freq_matrix)    
    rel_freq_across_files = np.sum(rel_freq_matrix, axis=0)/rel_freq_matrix.shape[0]
    
    #it is easier to continue with a np.matrix here than a list
    #rel_freq_list = rel_freq_matrix.tolist()
    
    return rel_freq_matrix, rel_freq_across_files
    
#COMMENT OUT TO RUN FUNCTION
# rel_matrix, rel_lists_avg = compute_centroid(list_2015[:5])
# print(rel_matrix, rel_lists_avg) # sum(rel_lists_avg) = 1 # rel_matrix.shape = (5, 26)


def taz_barplot(list1, list2) -> None:
    
    _, avg1 = compute_centroid(list1)
    _, avg2 = compute_centroid(list2)
    
    letters = string.ascii_lowercase
    letters_list = list(letters)
    x_axis = np.arange(26)
    #print(avg1)
    #print(avg2)
    
    #fig, ax = plt.subplots(1,1, sharex=True, sharey=True)
    ax = plt.subplot(111)
    ax.bar(x_axis-0.2, avg1, width=0.4, label="2015")
    ax.bar(x_axis+0.2, avg2, width=0.4, label="2018")
    ax.set_title("Barplot of relative letter frequencies compared between years")
    plt.xticks(x_axis, letters_list)
    plt.legend()
    plt.savefig(os.path.dirname(path)+r'/bar_plot.png', dpi=300)
    plt.show()
    
    return
    
#COMMENT OUT TO RUN FUNCTION   
# taz_barplot(list_2015, list_2018)

def taz_scatterplot(list1, list2, two_letters: str) -> None:
    
    list2015, _ = compute_centroid(list1)
    list2018, _ = compute_centroid(list2)
    
    two_letters = list(two_letters)
    two_index = [(ord(i) - ord("a")) for i in two_letters]
    
    ax = plt.subplot(111)
    ax.scatter(list2015[:,two_index[0]], list2015[:,two_index[1]], label="2015")
    ax.scatter(list2018[:,two_index[0]], list2018[:,two_index[1]], label="2018")
    ax.set_xlabel(two_letters[0])
    ax.set_ylabel(two_letters[1])
    ax.set_title("relative letter frequency compared between years")
    plt.legend()
    plt.savefig(os.path.dirname(path)+r'/scatter_plot_'+''.join(two_letters)+r'.png', dpi=300)
    plt.show()
    
    return

#COMMENT OUT TO RUN FUNCTION
#taz_scatterplot(list_2015, list_2018, "ae")
# taz_scatterplot(list_2015, list_2018, "ms")
# taz_scatterplot(list_2015, list_2018, "mi")
# taz_scatterplot(list_2015, list_2018, "ei")


#wenn ich die drei graphen vergleiche, fällt mir nichts besonderes auf.
#wieso sollte sich denn die benutzung einzelner buchstaben im laufe von nur
#drei jahren ändern? bei mir sieht aber auch der "ae" scatter-plot nicht genau so
#aus wie auf dem übungsblatt.











