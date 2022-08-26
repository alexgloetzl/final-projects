from cProfile import label


def generate_sequences(length: int, n: int):
    """
    generate a list of n random dna-sequences elements of length "Length"
    """
    dnas = []
    bases = [i for i in "ATGC"]
    for i in range(n):
        my_dna = random.choices(bases, weights=[0.25, 0.25, 0.25, 0.25], k=length)
        my_dna = ''.join(my_dna)
        dnas.append(Seq(my_dna))

    return dnas

def generate_prefixes(reads: list, prefix_len: int, p: int) -> list:
    """
    reads: list of reads
    prefix_len: length of prefixes of those reads
    p: how many prefixes are supposed to be returned
    """
    my_prefixes = [read[:prefix_len] for read in reads]
    return random.sample(my_prefixes, p)

def search_readsInList(reads: list, prefixes: list):
    """
    compares every read with every prefix given. if it matches
    it returns the matched reads in a list. execution time of function
    is also measured.
    """
    tic = timeit.default_timer()
    matching_reads = []
    for read in reads:
        for pre in prefixes:
            if read[:len(pre)] == pre:
                matching_reads.append(read)

    toc = timeit.default_timer()
    return matching_reads, toc-tic

def search_reads_in_dict(reads: list, prefixes: list):
    tic = timeit.default_timer()

    #make_suffix_dict takes length of suffixes as argument
    my_suffix_table = \
        make_suffix_dict(reads, len(reads[0])-len(prefixes[0]), verbose = False)

    matching_reads = []
    for pre in prefixes:
        if pre in my_suffix_table:
            #my_concat = pre+my_suffix_table[pre]
            #print(pre, my_suffix_table[pre])
            for suff in my_suffix_table[pre]:
                matching_reads.append(Seq(pre)+suff)

    toc = timeit.default_timer()
    return matching_reads, toc-tic

if __name__ == "__main__":

    from Bio.Seq import Seq
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    import timeit
    from make_suffix_dict import make_suffix_dict
    import matplotlib.pyplot as plt

    times = []
    my_range = np.arange(10,1001,10)
    for N in my_range:
        #print("N: ", N)
        my_sequences = generate_sequences(50, N) #N reads of len=50
        #print(my_sequences[:5])

        my_prefixes = generate_prefixes(my_sequences,20,N) #N prefixes of len=20
        #print(my_prefixes)

        matched_reads, my_time_nested = search_readsInList(my_sequences, my_prefixes)
        #print(my_time_nested)

        matched_reads2, my_time_dict = search_reads_in_dict(my_sequences, my_prefixes)
        #print(my_time_dict)

        times.append([my_time_nested, my_time_dict])

    times_arr = np.array(times)
    plt.plot(my_range,times_arr[:,0],label="nested")
    plt.plot(my_range,times_arr[:,1],label="hash")
    plt.legend()
    plt.xlabel("number of reads N")
    plt.ylabel("time [s]")
    plt.title("comparision between computation\ntime of nested and hash")
    plt.tight_layout()
    plt.savefig("blatt6_C_nested_hash_time_measured.png",dpi=300)
    plt.show()


