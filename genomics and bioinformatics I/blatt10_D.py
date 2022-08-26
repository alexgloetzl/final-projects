# %%
import numpy as np
import string
import os

def swAlign(seq1, seq2, match=1, mismatch=-1, indel=-1, verbose=True):
    my_matrix = np.ndarray( (len(seq2)+1, len(seq1)+1))
    my_matrix[:,:] = 0.0

    for i in range(1, len(seq2)+1):
        for j in range(1, len(seq1)+1):
            if seq2[i-1] == seq1[j-1]:
                m_temp = my_matrix[i-1, j-1] + match   # match
            else:
                m_temp = my_matrix[i-1, j-1] + mismatch   # mismatch
            indent_left = my_matrix[i, j-1] + indel          # indel
            indent_up = my_matrix[i-1, j] + indel          # indel
            temp = max(0, m_temp,indent_left, indent_up)
            my_matrix[i, j] = temp

    if verbose:
        print(my_matrix)

    return my_matrix, np.max(my_matrix)

if __name__ == '__main__':

    seq1 = 'ccatctgg' #oben
    seq2 = 'cctttagg' #links

    wmatrix, maxscore = swAlign(seq1, seq2, verbose=True)
    print("Score:", maxscore)


    path = r"C:\Users\aleX\Kurse\genomikI\week10\program_code"

    py_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if name[-3:] == ".py":
                py_files.append(os.path.join(dirpath, name))

    py_code = []
    for file in py_files:
        with open(file, encoding = 'utf-8') as f:
            code = f.read()
            printable_code = ""
            for letter in code:
                if letter in string.printable[:93]:
                    printable_code += letter

        py_code.append(printable_code)

    #print(py_code[0])

    score_matrix = np.ndarray((len(py_files), len(py_files)))
    score_matrix[:,:] = 0
    for i, i_code in enumerate(py_code):
        for j, j_code in enumerate(py_code):
            #man koennte auch nur die hälfte der scores berechnen wegen symmetrie,
            #aber eigentlich ganz guter sanity-check
            score_matrix[i,j] = swAlign(i_code, j_code, verbose=False)[1]

    print(score_matrix)

    #console output:
    # [[ 814.   36.   92.   35.   65.  418.]
    # [  36. 1074.   92.   64.   55.   46.]
    # [  92.   92. 1225.   51.   53.   46.]
    # [  35.   64.   51.  869.   40.   36.]
    # [  65.   55.   53.   40. 1182.   56.]
    # [ 418.   46.   46.   36.   56.  825.]]

    #laut tabelle sind also 01.py und 06.py recht ähnlich. dies bestätigt ein blick in den code.