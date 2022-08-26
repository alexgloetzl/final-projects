from Bio import SeqIO
from Bio.Seq import Seq
import matplotlib.pyplot as plt
import numpy as np
#from ..week4.blatt4_C import count_orf

def count_orf(my_seq):

    seq_length = len(my_seq)
    my_orf_total = []
    start_stop_indices = []
    for base in [my_seq, my_seq.reverse_complement()]:
        for frame in range(3):
            length = seq_length-(seq_length%3) #seq length in multiple of three
            curr_seq = base[frame:frame+length] #for mod(len(curr_seq), 3) = 0 or 1 OUT OF BOUNDS for biopython; biopython expects multiple of triblets
            curr_length = len(curr_seq)
            fixed_seq = curr_seq + "N"*((3-curr_length%3)%3) #adds seq+'N' or seq+'NN'
            #print(len(fixed_seq))
            #print(curr_seq)
            start = frame+1+154346345#starts counting at 1, not zero for convenience
            for protein in fixed_seq.translate().split("*"): # '*' equals stop
                my_orf_total.append(protein)
                start_stop_indices.append([start, start+3*len(protein)-1])
                start += 3*len(protein)+3


    #my_orf = my_orf_total[1::2]
    my_orf_lengths = [len(i) for i in my_orf_total]
    return my_orf_total, start_stop_indices, my_orf_lengths

if __name__ == "__main__":

    path1 = r"./makeDictionaries/chrX_region.fna"
    path2 = r"./makeDictionaries/test.fna"

    reads = []
    for read in SeqIO.parse(path1, "fasta"):
        reads.append(read.seq)
        #print(type(read))

    orf_proteins, start_stop, orf_lengths = count_orf(reads[0])
    print("mean: ", np.mean(orf_lengths))
    print("max: ", np.max(orf_lengths))
    plt.hist(orf_lengths,bins=30)
    plt.xlabel("length of ORF's")
    plt.ylabel("counts")
    plt.tight_layout
    plt.savefig("partB_hist_orf.png",dpi=300)
    plt.show()

    print("answer to question:")
    #the comparison to the histogram of last week's exercise C
    #shows that the shape stayed the same but the length of
    #both the mean and max of the ORFs in the chrX_region
    #are twice as long.

    my_zip = list(zip(orf_proteins, start_stop, orf_lengths))
    biggest_orfs = sorted(my_zip, key=lambda x: x[2], reverse=True)
    # print(*biggest_orfs[:10], sep='\n')
    # Output:
    # (Seq('PQGKEMLGRQSRRGEVPPGLRAQQRGTRADGPNPAAGSRGGGWWRCGESPEQHH...APQ'), [154389020, 154390585], 522) #half a gene
    # (Seq('AGNGCGRRVDAVMGGGDGWAGSWASGRVGVRFPVQRAGVGKMGGRRGSDPGSPG...PQK'), [154362792, 154364099], 436) #gene
    # (Seq('PRPALLFVLMTDGWPIWQAAWARPCPCLVRAGSQGKGRQVESQAGGLGSGHSVA...GSS'), [154439690, 154440796], 369) #gene
    # (Seq('LCFFLAPRLPVCVWGGRSKLVVGAISDGRPILQGHKEPRAPDNGTHELQPTLQN...TAL'), [154370291, 154371304], 338) #gene
    # (Seq('QETLHGRAPSRLLREGHQPRETTTLSLTSKSSACGSASVDRSVAMSGKNHGPPP...GGD'), [154409555, 154410553], 333) #gene
    # (Seq('VTMERPPPPPTPNSAHKGPERPPDMPVGAGVFANICRGTGCPRHMDSLQGPAEA...RPP'), [154386064, 154387023], 320) #not a gene!
    # (Seq('VGRELQVAGDVAFMSVGRRSPQVPGRAQKRCCQTGAHVDWSSVAGRFAASPRAR...SLF'), [154371349, 154372272], 308) #gene
    # (Seq('AVSGAGLLGLQPARLTRDFPSPGPLRGVGWLSSLSHLGSAPSLHIPTPRRHPPS...SGR'), [154371642, 154372541], 300) #gene
    # (Seq('AASPAAGNPPGAGRLAGKAGLPRKHWAGPSGPMGAGTSPAGVPRHPPAGRPAGG...PRQ'), [154389172, 154390047], 292) #not a gene!
    # (Seq('LEGRGPCFLPAGSPFSVKVTGEGRVKESITRRRRAPSVANVGSHCDLSLKIPGR...GGA'), [154447757, 154448620], 288) #gene

    #website: http://www.ensembl.org/Homo_sapiens/Location/View?r=X:154447757-154448620;db=core