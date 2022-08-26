from extendContig.readReads import read_reads
from extendContig.makeDictionaries import make_suffix_dict
from extendContig.makeDictionaries import make_prefix_dict
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq


def find_extension_right(contig: str, reads: str):
    """
    contig:
        contig to be extended to the right
    reads:
        available reads
    returns:
        function return smalles extension for the right end of the contig from reads considered for extension
    """

    suffix_dict = []
    for extension in np.arange(1,11): #hardcoded because extension length is not specified as wanted parameter
        suffix_dict.append(make_suffix_dict(reads, ext_size = extension))

    flag = 0

    for slice in range(len(contig)):
        #slice original contig up. starting with the original length and slowly making it smaller.
        sliced_contig = contig[slice:]
        #print(slice)
        if flag != 1:
            #first elements in suffix_extension have the smallest extensions. these we want.
            for suffix_extension, _ in enumerate(suffix_dict):
                if sliced_contig in suffix_dict[suffix_extension]:
                    #print("contig: ", sliced_contig, "suffix: ", suffix_dict[suffix_extension][sliced_contig][0])
                    contig += suffix_dict[suffix_extension][sliced_contig][0]
                    flag = 1
                    reads.remove(sliced_contig+suffix_dict[suffix_extension][sliced_contig][0])
                    break #break after we found our minimal extension

    return contig, reads


def find_extension_left(contig: str, reads: str):
    """
    contig:
        contig to be extended to the left
    path_reads:
        path to reads
    returns:
        function return smalles extension for the right end of the contig from reads considered for extension
    """

    prefix_dict = []
    for extension in np.arange(1,11): #hardcoded because extension length is not specified as wanted parameter
        prefix_dict.append(make_prefix_dict(reads, ext_size = extension))

    flag = 0

    for slice in range(len(contig)):
        sliced_contig = contig[:-slice if slice != 0 else None]
        if flag != 1:
            for prefix_extension, _ in enumerate(prefix_dict):
                if sliced_contig in prefix_dict[prefix_extension]:
                    contig = prefix_dict[prefix_extension][sliced_contig][0] + contig
                    flag = 1
                    reads.remove(prefix_dict[prefix_extension][sliced_contig][0]+sliced_contig)
                    break

    return contig, reads

def extend_contig(contig, reads):
    '''
    contig:
        contig to extend
    reads:
        starting reads
    returns:
        extended reads
    '''
    suffix_dict = []
    for extension in np.arange(1,11): #hardcoded because extension length is not specified as wanted parameter
        suffix_dict.append(make_suffix_dict(reads, ext_size = extension))

    new_contig = contig
    rest_reads = reads
    diff = 1
    while diff > 0: #maximal right extension
        diff = 0
        old_contig = new_contig
        new_contig, rest_reads = find_extension_right(old_contig, rest_reads)
        diff = len(new_contig) - len(old_contig)

    diff = 1
    while diff > 0: #maximal left extension
        diff = 0
        old_contig = new_contig
        new_contig, rest_reads = find_extension_left(old_contig, rest_reads)
        diff = len(new_contig) - len(old_contig)

    return new_contig


if __name__ == "__main__":
    #ANSWER TO QUESTONS:
    #in line 27 & 28 ":"-operator is used to slice a list.
    #explanation of line 26: enumerate iterates over the index of a iterable (e.g. a list) and let's us access it
    #       by defining a tuple pair like in line 26: (i, read).

    path = r".\extendContig\test.fna"
    my_reads = read_reads(path)

    #to test if it works
    my_ext_contig_right, _ = find_extension_right(Seq("TAATGC"), my_reads, )
    #to test if it works
    my_ext_contig_left, _ = find_extension_left(Seq("TCCCTGCAGCG"), my_reads)

    #this should print out the full read from test.fna
    full_extension = extend_contig("GATAATG", my_reads)
    print(full_extension)

    #now to the real data set smallReads1.fna
    path = r".\extendContig\smallReads1.fna"
    my_reads = read_reads(path)

    full_extension2 = extend_contig("TTGATGGTAGAGTTGATGGTCAAGTAGACTTATTTAGAAATGCCCGTAATGGTGTTCTTATTACAGAAGGTAGTGT", my_reads)
    print(full_extension2)

    #i don't have the last part of the D exercise.





