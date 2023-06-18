# -*- coding: utf-8 -*-
"""
Created on Thu May 12 19:32:03 2022

@author: aleX
"""
import matplotlib.pyplot as plt
import numpy as np

def fragment_genome(n:int, p: float) -> list:
    '''
    Parameters
    ----------
    n : int
        length of genome in units of base pairs (bp's)
    p : float
        probability of a cut between base pairs

    Returns
    -------
    list
        a list of containing the resulting fragment lengths
    '''
    
    my_genome = [*range(n)]
    my_cuts = [np.random.choice(2,p=[1-p,p]) for i in range(n)] 
    #my_cuts beispielsweise:
    #[0, 0, 1, 0, 0, 0, 0, 1, 1, 0]    
    #dabei stehen die '1'er fuer cuts nach dem jeweiligem index
    # 1 = cut
    # 0 = non-cut
    
    #print(my_cuts)
    my_list = []
    begin_cut = 0      #first cut is the beginning of the genome so to say
    for i in range(n):
        if my_cuts[i] == 1:
            my_list.append(my_genome[begin_cut:i+1])
            begin_cut = i+1
            
    #print(my_list)
    my_lengths = [len(i) for i in my_list]
    #print(my_lengths)
    return my_lengths


def hist_fragment_lengths(my_lengths: list, n: int, p: int) -> dict:
    '''
    Parameters
    ----------
    my_lengths : list
        a list of fragment lengths
    n : int
        length of genome in units of base pairs (bp's)
    p : int
        probability of a cut between base pairs

    Returns
    -------
    dict
       returns a dictionary containing the mean, median, maximum and minimum fragment
       lengths
    '''
    #print(my_lengths)
    plt.hist(my_lengths, bins=50)
    plt.xlabel("Fragment Lengths")
    plt.ylabel("Frequency")
    plt.title(f"n: {n} bp | p: {p}")
    plt.savefig(r"./hist_prob_"+str(p)+r".png", dpi=300)
    plt.show()
    my_aggregations = ["mean", "median", "max", "min"]
    my_dict = {i:0 for i in my_aggregations}
    
    my_dict["mean"] = np.mean(my_lengths)
    my_dict["median"] = np.median(my_lengths)
    my_dict["max"] = np.max(my_lengths)
    my_dict["min"] = np.min(my_lengths)
    #print(my_dict)
    return my_dict
    


if __name__ == "__main__":
    
    N = 100000
    p = [0.01,0.005,0.001]
    
    my_lengths = []
    for pp in p:
        my_temp_len = fragment_genome(N,pp)
        my_lengths.append(my_temp_len)
    
        my_aggregates = hist_fragment_lengths(my_temp_len, N, pp)
        print("aggregates with probability: ",pp)
        print(my_aggregates)
        


    










