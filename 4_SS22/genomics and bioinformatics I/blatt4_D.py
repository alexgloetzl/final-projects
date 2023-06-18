#%%

#part A, template heißt, dass man's erst
#in rna umwandeln muss und dann dort die codons suchen muss
def read_reads(path: str, verbose: str = False, subset=None) -> list:
    '''
    Parameters
    ----------
    path : str
        path to the fasta file
    verbose : str
        *prints total amount of reads stored in input file
        *prints amount of duplicated reads removed
        *prints amount of unique reads returned
    subset : 
        if False all reads in file are used
        if True only a subset of reads in file is used

    Returns
    -------
    list
        list of reads in the fasta file
    '''
    my_reads = []
    with open(path) as handle:
        for record in SeqIO.parse(handle, "fasta"):
            my_reads.append(record.seq)
            #print(record.id)

    if subset or subset == 0: #(if default value of subset=False (instead of subset=None) would lead to interpreting 0 as False and therefore assigning max subset when subset=0)
        if isinstance(subset,int) and 0 < subset < len(my_reads)+1:
            random_subset = random.sample(my_reads, k=subset)
        else:
            print(subset)
            print(f"subset is out of range or not an integer! range of subset is 0 to {len(my_reads)}.")
            raise TypeError()
    else: 
        random_subset = my_reads #reference, not a copy

    unique = []
    duplicate_counter = 0
    for read in random_subset:
        if read not in unique:
            unique.append(read)
        else:
            duplicate_counter +=  1 

    if verbose: curr_unique = len(random_subset)

    #duplicate_counter_after_rev = 0
    for read in unique:
        my_rev = read.reverse_complement()
        if my_rev not in unique:
            unique.append(my_rev)
        # else:
        #     duplicate_counter_after_rev +=  1


    if verbose:
        print("number of input reads: ", len(my_reads))
        if subset: print("subset of input reads used: ", subset)
        print("number of duplicates: ", duplicate_counter)
        print("number of unique's before adding rev-complements: ", curr_unique)
        print("unique reads: ", len(unique))

    return unique



if __name__ == "__main__":

    from Bio import SeqIO
    from Bio.Seq import Seq
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    import random

    path = r".\smallReads"

    #record = SeqIO.read(r".\smallReads1", "fasta")
    fna_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if name[-3:] == "fna":
                fna_files.append(os.path.join(dirpath, name))
    
    print(fna_files)

    test_read = read_reads(fna_files[2], verbose=True,subset=None) #fna_files[2] was a much smaller test set

    sampling = [500,1000,3000,6000,12000,25000,50000,75000,100000]
    sampling2 = [*range(1,681,50)] #test
    
    plot_unique = []
    for i in sampling2: #test
        #print(i)
        plot_unique.append(len(read_reads(fna_files[2], verbose=False, subset=i)))

    plt.title("unique reads in dependence of sample size")
    plt.plot(sampling2, plot_unique,label="uniques")
    #plt.plot(sampling2,sampling2,label="identidy line")
    plt.xlabel("subset")
    plt.ylabel("unique reads")
    plt.legend()
    #print(plot_unique)
    plt.savefig(r"./reads_subset.png", dpi=300)
    plt.show()

    #answers to questions asked in exercise sheet:
    #3, the new list does not only contain unique reads because the file has both
    #   coding and template strands.
    #4, in my case the relationship was linear (only used a small test set) as can
    #   be seen in the graph 'reads_subset.png'.