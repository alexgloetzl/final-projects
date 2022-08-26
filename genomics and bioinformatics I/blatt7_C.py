import timeit
import numpy as np
from numpy import random
import matplotlib.pyplot as plt

def generate_sequences(n, l, p):
    my_seq = []
    for i in range(n): 
        my_seq.append(np.random.choice([0, 1], replace=True, size=l, p=[1-p, p]))

    return my_seq

def longest_head_run_length(seq):
    max_counter = 0
    counter = 0
    for i in np.arange(1,len(seq),1):
        if seq[i-1] == 1 and seq[i] == 1:
            counter += 1
            #print(counter)
            max_counter = max(max_counter, counter)
        else:
            counter = 0

    return max_counter + 1

if __name__ == "__main__":

    #probability: 0.5**n to have head run of length n
    #probability for twice as likely: (2/3)**n 

    # tic = timeit.default_timer()
    # n = 1000000
    # seqs = []
    # for i in range(n):
    #     seqs.append(random.choice([0, 1]))
    # toc = timeit.default_timer()
    # print("method 1: ",toc-tic) #12.113230399999999 sec


    # tic = timeit.default_timer()
    # n = 1000000
    # seqs = np.zeros(n)
    # indices = np.random.choice(np.arange(n), replace=False, size=int(0.5*n))
    # seqs[indices] = 0
    # toc = timeit.default_timer()
    # print("method 2: ", toc-tic) #0.041437500000000016 sec


    # tic = timeit.default_timer()
    # n = 1000000
    # seqs = [random.randint(0,1) for i in range(n)]
    # toc = timeit.default_timer()
    # print("method 3: ", toc-tic) #2.8621284 sec


    # my_seq = generate_sequences(10, 100, 0.7)
    # print(my_seq[0])
    # longest = longest_head_run_length(my_seq[0])
    # print(longest)

    #3,
    my_seq = generate_sequences(10000, 70, 0.25)
    longest_heads = []
    for i in my_seq:
        longest_heads.append(longest_head_run_length(i))
    
    longest_heads = np.array(longest_heads)
    #print(longest_heads)
    #print(np.arange(len(longest_heads))[longest_heads > 6])
    seven_heads_in_row = len(longest_heads[longest_heads > 6])
    print("more than seven heads in row: ", seven_heads_in_row)
    # more than seven heads in row:  2271 / 10000 = 0.2271

    #this means that in more than 20% of the cases, there are
    #head runs of length 7 or more. this makes the rat-human comparison
    #not very remarkable

    #4,
    avg_longest_per_length = []
    for i in np.arange(0,201,10):
        my_seq = generate_sequences(1000, i, 0.25)
        longest_seq_list = []
        for j in my_seq:
            longest_heads = longest_head_run_length(j)
            longest_seq_list.append(longest_heads)

        longest_seq_list = np.array(longest_seq_list)
        my_avg = np.mean(longest_seq_list)
        avg_longest_per_length.append(my_avg)

    plt.plot([*np.arange(0,201,10)], avg_longest_per_length)
    plt.xlabel("length of sequence")
    plt.ylabel("average length of longest head run")
    plt.title("plot of average head run length\nin dependence of sequence length")
    plt.tight_layout()
    plt.savefig("blatt7_C_average_head_run_length.png",dpi=300)
    plt.show()