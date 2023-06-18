# -*- coding: utf-8 -*-
"""
Created on Fri May 13 07:52:45 2022

@author: aleX
"""
def sliding_window(my_seq, window_len:int, step_size:int) -> list:
    '''
    Parameters
    ----------
    my_seq : TYPE
        a dna sequence (from SeqIO)
    window_len : int
        length of the sliding window
    step_size : int
        step size of window

    Returns
    -------
    list
        list of CpG frequencies in the windows
    '''
    cg_window_freq = []
    for window_start in np.arange(0,len(my_seq),step_size):
        counter = 0
        #print(my_seq[window_start : window_start+window_len-1])
        #we dont go fully to the end of the window. we stop two bases before
        for i, base in enumerate(my_seq[window_start : window_start+window_len-1]): 
            base_ind = i + window_start #actual base index in whole sequence
            if my_seq[base_ind:base_ind+2] == Seq("CG"):
                counter += 1
                #print(my_seq[i:i+2])
                
        cg_window_freq.append(counter/(window_len//2)) #because of "dinucleotides"
                    
    return cg_window_freq



if __name__ == "__main__":

    from Bio import SeqIO
    from Bio.Seq import Seq
    import matplotlib.pyplot as plt
    import numpy as np
    
    path = r".\chrX_region.fna"
    
    for seq_record in SeqIO.parse(path, "fasta"):
        my_seq = seq_record.seq
    
    
    my_cg_frequencies = sliding_window(my_seq, window_len=1000, step_size=1000)
    print(my_cg_frequencies)
    
    
    plt.plot([*range(len(my_cg_frequencies))],my_cg_frequencies)
    plt.xlabel("number of sliding windows")
    plt.ylabel("relative frequency of 'CG' in window")
    plt.title("Sliding Window for CG frequencies")
    plt.savefig(r"./sliding_window.png", dpi=300)
    plt.show()
    
    
    #on website:
    #https://www.ensembl.org/Homo_sapiens/Location/View?r=X:154346345-154454120
    #configure region image -> search for track "cpg islands" -> activate it
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    