import Bio.SeqIO
import Bio.Seq
import matplotlib.pyplot as plt
import os
from readReads import read_reads #readReads is in the same directory as the main program blatt5.py

def make_suffix_dict(reads: list, suffix_len: int) -> dict():

    #my_suff_table = {read[:-suffix_len]: read[-suffix_len:] for read in reads}
    my_suff_list = list((read[:-suffix_len],read[-suffix_len:]) for read in reads)
    #print(my_suff_list)
    my_dict = dict()
    for key, value in my_suff_list:
        if key in my_dict:
            if not isinstance(my_dict[key],list):
                my_dict[key] = [my_dict[key],value]
            else:
                my_dict[key].append(value)

        else:
            my_dict[key] = value

    return my_dict

def make_prefix_dict(reads: list, prefix_len: int) -> dict():

    my_pref_list = list((read[prefix_len:],read[:prefix_len]) for read in reads)
    #print(my_pref_list)
    my_dict = dict()
    for key, value in my_pref_list:
        if key in my_dict:
            if not isinstance(my_dict[key],list):
                my_dict[key] = [my_dict[key],value]
            else:
                my_dict[key].append(value)

        else:
            my_dict[key] = value

    return my_dict

def create_suffix_dict(reads: list, suffix_len_max: int) -> dict():

    my_dicts = []
    for my_len in range(1,suffix_len_max,1):
        my_dicts.append(make_suffix_dict(reads,my_len))
    
    return my_dicts

def create_prefix_dict(reads: list, prefix_len_max: int) -> dict():

    my_dicts = []
    for my_len in range(1,prefix_len_max,1):
        my_dicts.append(make_prefix_dict(reads,my_len))
    
    return my_dicts

if __name__ == "__main__":

    path1 = r"./makeDictionaries/firstReads.fna"
    path2 = r"./makeDictionaries/conflictReads.fna"

    reads = []
    for path in [os.path.join("makeDictionaries",fna_files) for fna_files in ["smallReads1.fna","smallReads2.fna"]]: #,"smallReads2.fna"
        #print(path)
        # for read in Bio.SeqIO.parse(path, "fasta"):
        #    reads.append(str(read.seq))
        temp_reads = (read_reads(path, subset = 1.0, verbose = False))
        for read in temp_reads:
            reads.append(read)

    #print(len(reads))
    print("for testing purposes of the previous tasks")
    # my_suff = make_suffix_dict(reads,17)
    # for key in my_suff:
    #    print(f"{key}: {my_suff[key]}")

    # my_pref = make_prefix_dict(reads,17)
    # for key in my_pref:
    #    print(f"{key}: {my_pref[key]}")

    dict_comparisons = []
    for prefix in range(1,76,1):
        dict_comparisons.append(len(make_prefix_dict(reads,prefix)))

    print(dict_comparisons[-1]) #prints 4 as expected since suffix will be either A,T,G or C and together they will match any prefix string
    #dict_key_len = [len(my_dict) for my_dict in dict_comparisons]
    plt.plot([*range(1,76)],dict_comparisons)
    plt.title("Prefix Table Plot")
    plt.xlabel("prefix length")
    plt.ylabel("key length of dictionaries")
    plt.tight_layout()
    plt.savefig("prefix_table_plot.png",dpi=300)
    plt.show()

    print("answer to questions:")
    # 10 lines of comments

    # line 41: a set allows no dubplicates, therefore we can use it to delete all the replicates in our reads-list.

    # line 57: if the program foo.py is executed as the main program then the "if __name__ == "__main__":"-Block
    # will be executed and __name__ will be set to __main__.
    # however if the program is only used as a module and is imported by another main program
    # then __name__ will be the name of the module, i.e. "foo", the if-clause will not be satisfied anymore
    # and the if-block will not be executed.
    
    # 2, conflict is occuring on the last (24th) base pair position
    # 3, see graph. with increasing prefix length the number of keys in the dictionary is decreasing

    print("also for testing purposes of the last task")
    # my_test = create_prefix_dict(reads,76)
    # my_lengths = [len(key) for key in my_test]
    # plt.plot([*range(1,76)],my_lengths)
    # plt.title("Prefix Table Plot")
    # plt.xlabel("prefix length")
    # plt.ylabel("key length of dictionaries")
    # plt.savefig("prefix_table_plot.png",dpi=300)
    # plt.show()
# %%
