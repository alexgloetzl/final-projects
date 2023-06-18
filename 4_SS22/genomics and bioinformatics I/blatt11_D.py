# %%
import numpy as np
import string
import os
import Bio.SeqIO
import Bio.Seq

def swAlign(seq1, seq2, match=1, mismatch=-1, indel=-1, plot_verbose=False, path_verbose=False):
    my_matrix = np.ndarray( (len(seq2)+1, len(seq1)+1))
    path_matrix = np.empty((len(seq2)+1, len(seq1)+1), dtype="<U1")
    my_matrix[:,:] = 0.0
    path_matrix[:,:] = "o"

    for i in range(1, len(seq2)+1):
        for j in range(1, len(seq1)+1):
            if seq2[i-1] == seq1[j-1]:
                m_temp = my_matrix[i-1, j-1] + match   # match
            else:
                m_temp = my_matrix[i-1, j-1] + mismatch   # mismatch
            indent_left = my_matrix[i, j-1] + indel          # indel
            indent_up = my_matrix[i-1, j] + indel          # indel
            max_temp = -np.inf
            path_temp = "xxx"
            for path_temp_i,max_temp_i in zip(["l","u","d"],[indent_left, indent_up,m_temp]):
                if max_temp_i >= max_temp:
                    if max_temp_i >-1:
                        max_temp = max_temp_i 
                        path_temp = path_temp_i
                    else:
                        max_temp = 0
                        path_temp = "o"

            my_matrix[i,j] = max_temp
            path_matrix[i,j] = path_temp

    if plot_verbose:
        print(my_matrix)
        print(path_matrix)


    #extension
    #first find max score and its position in my_matrix
    max_temp = 0     
    max_indices = (0,0)      
    for i in range(0, len(seq2)+1):
        for j in range(0, len(seq1)+1):
            if my_matrix[i,j] > max_temp:
                max_temp = my_matrix[i,j]
                max_indices = (i,j)
    i,j = max_indices
    seq1a = ""        
    seq2a = ""        

    limit = 0
    while i > 0 and j > 0:
        if my_matrix[i,j] <= limit:
            break

        if path_matrix[i,j] == "d":
            seq1a = seq1[j-1] + seq1a
            seq2a = seq2[i-1] + seq2a
            j = j - 1
            i = i - 1
        elif path_matrix[i,j] == "u": #bei mir ist die regel hier ein wenig anders, weil ich seq1 als "obrige" seq gewählt habe
            seq1a = "-" + seq1a
            seq2a = seq2[i-1] + seq2a
            i = i - 1
        elif path_matrix[i,j] == "l":
            seq1a = seq1[j-1] + seq1a
            seq2a = "-" + seq2a
            j = j - 1

    if path_verbose:
        for i in np.arange(0,len(seq1a),80):
            print("seq1:", seq1a[i:i+80]) 
            print("seq2:", seq2a[i:i+80]) 
            print()

    return my_matrix, np.max(my_matrix), [seq1a, seq2a]

if __name__ == '__main__':

    seq1 = 'ccatctgg' #oben
    seq2 = 'cctttagg' #links

    print("seq1 and seq2:")
    wmatrix, maxscore, _ = swAlign(seq1, seq2, plot_verbose=True, path_verbose=True)
    #das alignment stimmt. ich bin auf das selbe ergebnis per hand gekommen.
    print("Score:", maxscore,"\n")

    print("20 times seq1 and seq2:")
    wmatrix, maxscore, _ = swAlign(seq1*20, seq2*20, plot_verbose=False, path_verbose=False)
    print("Score:", maxscore)


    path = r"C:\Users\aleX\Kurse\genomikI\week11\smith_waterman"
    fna_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if name[-4:] == ".fna":
                fna_files.append(os.path.join(dirpath, name))

    reads = []
    for file in fna_files:
        for read in Bio.SeqIO.parse(file, "fasta"):
            reads.append(str(read.seq))
    
    reads = sorted(reads, key=lambda x: len(x), reverse=False)
    # 1st element = homo sapiens
    # 2nd element = zebrafish

    print("\n")
    wmatrix, maxscore, aligns = swAlign(reads[0], reads[1], path_verbose=False)
    print("maxscore:", maxscore)
    print("transcript length homo sapiens: ", len(reads[0]))
    print("transcript length zebrafish: ", len(reads[1]))
    print("alignment length: ", len(aligns[0]))

    print("\n")
    wmatrix2, maxscore2, aligns = swAlign(reads[0], reads[1], indel=-2)
    print("maxscore:", maxscore2)
    print("alignment length: ", len(aligns[0]))

    #the alignments are so different because we punish gaps more
    #and therefore the algorithm is inclined to make shorter
    #alignments instead of continuing the alignment through the "gaps"-area
    #to the next area with a high "score". 


    #console output for 3rd exercise:
    # maxscore: 634.0
    # transcript length homo sapiens:  2408
    # transcript length zebrafish:  2620
    # alignment length:  2130

    # maxscore: 435.0
    # alignment length:  1449
