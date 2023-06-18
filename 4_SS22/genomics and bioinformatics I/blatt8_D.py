from collectContigsRC.ReadReads import readFasta
from collectContigsRC.ReadDictionary import makeSuffixDicts
from collectContigsRC.ExtendContigRC import extendContig
import regex as re
import numpy as np

def assemble_contigs(reads:list[str], max_len: int) -> list:
    """
    func assembles all possible contigs from list with a maximal
    extension length of max_len 
    """

    my_suff_dict = makeSuffixDicts(reads, max_len)

    all_extended_contigs = []
    for read in reads:
        contig = extendContig(read, reads, my_suff_dict, verbose = False)
        all_extended_contigs.append(contig)

    return all_extended_contigs


def map_to_reference(contigs:list[str], reference:str):
    """
    matches available contigs to reference genome.
    returns list of matching contigs, where the elements of the list
    are: start_index, end_index, length of contig
    """
    start_end = []
    for i_contig in contigs:
        match = re.search(i_contig,reference[0])
        #print(bool(match))
        if bool(match):
           start_end.append([match.start(),match.end()-1,len(i_contig)])

    return start_end


def get_Number(contigs:list[str], cov_perc):

    #wenn die concatenierte länge der contigs 50% des reference genomes
    #decken soll, muss das reference genome zweimal so lange sein.
    contig_len = np.array([len(i) for i in contigs])
    reference_genome_length = np.sum(contig_len)*(1/cov_perc)

    ordered = sorted(contigs, key=lambda x: len(x), reverse=True)
    total_length = 0
    lowest_contig_len = -1
    for i in ordered:
        total_length += len(i)
        if total_length > cov_perc * reference_genome_length:
            lowest_contig_len = len(i)
            break

    return lowest_contig_len

if __name__ == "__main__":
    """
    erklärung zu den fragen:
    zeile 52:   wenn das dictionary keine keys beinhaltet, kann es auch nicht 
                zur erweiterung genutzt werden und wird darum übergangen im 
                for-loop.
    zeile 81:   while loop mit bedingung True läuft ewig. in unserem fall haben
                wir eine break-bedingung. deshalb ist es ok.
    ExtendContigRC:
                der trick besteht darin nur ein find_extend_right() zu machen
                und dann am ende das reverse komplementäre des contigs zu bilden.
                dadurch wird beim nächsten for-loop durchlauf "reverse" beim
                find_extend_right() tatsächlich find_extend_left() durchgeführt
                (es wird also von 3' zu 5' erweitert). das wir das komplementäre
                contig bilden ist kein problem, weil wir in unseren reads, aus
                denen der suffix table gebildet wird,sowieso immer sowohl coding 
                strand als auch template haben.
                vorteil: es werden nur halb so viele dictionaries gebildet.
                nachteil: vielleicht leichter overhead durch reverse_complement().
                          muss zweimal ausgeführt werden.
                vorteil (RAM): nur halb so viele dictionaries werden alloziert.
                               nur suffix_dict und nicht auch noch prefix_dict.
    """

    my_reads = readFasta("smallReads1.fna", subset = 7000)

    all_contigs = assemble_contigs(my_reads, 30)

    ordered = sorted(all_contigs, key=lambda x: len(x), reverse=True)
    for i in ordered:
        print(len(i), end=", ")

    #console-output:
    #17272, 10374, 8358, 4043, 3479, 1645, 1568, 1313, 1142, 1131, 1021, 985, 896, 838, 812, 799, 691, 583, 485, 450, 367, 350, 263, 259, 251, 227, 212, 210, 184, 169, 167, 160, 160, 155, 149, 145, 133, 127, 121, 118, 115, 114, 113, 110, 101, 100, 98, 97, 94, 91, 89, 86, 83, 77, 77, 77, 76,
    #read und reverse-komplementärer read davon sollten nach extension
    #die gleiche länge haben. ist bei mir aber nicht so.

    my_ref = readFasta("GCF_000864885.1_ViralProj15500_genomic.fna", subset = 1)
    #print(my_ref)
    my_mapping = map_to_reference(all_contigs, my_ref)
    print(my_mapping)

        #nur die hälfte der contigs matched, weil die andere hälfte aus
        #reverse komplementären besteht und daher nicht matchen kann.


    #3,
    #5000 reads with coverage of 50%:
    my_reads2 = readFasta("smallReads1.fna", subset = 5000) 
    N50 = get_Number(all_contigs, 0.5)   
    print(N50)

    #7000 reads with coverage of 70%:
    my_reads2 = readFasta("smallReads1.fna", subset = 7000) 
    N70 = get_Number(all_contigs, 0.7) 

    #12000 reads with coverage of 90%:
    my_reads2 = readFasta("smallReads1.fna", subset = 12000) 
    N90 = get_Number(all_contigs, 0.9) 

    #4, 
    my_reads = readFasta("smallReads1.fna", subset = 5000)

    all_contigs = assemble_contigs(my_reads, 50)
    #die gefahrt besteht, dass man nicht das richtige read als suffix/prefix auswählt, wenn die übereinstimmung-
    #länge/extensionlänge nicht groß genug ist.