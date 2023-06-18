def random_dna(length: int):
    bases = [i for i in "ATGC"]
    my_dna = random.choices(bases, weights=[0.3, 0.3, 0.2, 0.2], k=length)
    my_dna = ''.join(my_dna)
    #print(my_dna)
    return Seq(my_dna)

#mostly copied from http://biopython.org/tutorial: "20.1.13 Identifying open reading frames"
def count_orf(my_seq):

    seq_length = len(my_seq)
    my_orf_total = []
    for base in [my_seq, my_seq.reverse_complement()]:
        for frame in range(3):
            length = seq_length-(seq_length%3) #seq length in multiple of three
            curr_seq = base[frame:frame+length] #for mod(len(curr_seq), 3) = 0 or 1 OUT OF BOUNDS for biopython; biopython expects multiple of triblets
            curr_length = len(curr_seq)
            fixed_seq = curr_seq + "N"*((3-curr_length%3)%3) #adds seq+'N' or seq+'NN'
            #print(len(fixed_seq))
            #print(curr_seq)
            for protein in fixed_seq.translate().split("*"): # '*' equals stop
                my_orf_total.append(protein)

    #print(my_orf_total)
    my_orf = my_orf_total[1::2] #FFF*AAA*GGG*CCC*DDD -> only AAA and CCC are proteins
    my_orf_lengths = [len(i) for i in my_orf]
    #print(my_orf)
    return my_orf_lengths


if __name__ == "__main__":

    from Bio import SeqIO
    from Bio.Seq import Seq
    import matplotlib.pyplot as plt
    import numpy as np
    import random

    random.seed(3)

    test_dna = random_dna(5)
    count_orf(test_dna)
    # test_dna = test_dna +"N"
    # print(test_dna)
    #print(test_dna)
    #test_dna2 = test_dna.translate()
    #print(test_dna2)

    fig, axes = plt.subplots(1,2, sharex=True)
    for ax, i in enumerate([10000, 50000]):
        curr_dna = random_dna(i)
        curr_lengths = count_orf(curr_dna)
        axes[ax].hist(curr_lengths,label=f"dna-len: {i}")
        axes[ax].set_xlabel("length of ORF's")
        axes[ax].set_ylabel("counts")
        axes[ax].legend()
        print("dna length: ", i)
        print("mean: ", np.mean(curr_lengths))
        print("max: ", np.max(curr_lengths))

    fig.suptitle("histogram of ORF lengths for \ntwo differently long DNA-sequences")
    fig.tight_layout() 
    plt.savefig(r"./histogram_orfs.png",dpi=300)
    plt.show()

