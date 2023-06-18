# %%
import random
import numpy as np
import matplotlib.pyplot as plt
import Bio.SeqIO
import Bio.Seq


def generate_sequence(length: int, weights = [0.25]*4):
    """
    generate a list of n random dna-sequences elements of length "Length"
    """
    bases = [i for i in "ATGC"]
    my_dna = random.choices(bases, weights=weights, k=length)
    my_dna = ''.join(my_dna)

    return my_dna


def score_motifs(dna_seq, profile):
    # print(profile.shape)
    profile[profile==0] = np.inf
    log_matrix = np.log2((profile*0.01)/0.25) #formula from wikipedia; 0.25 is prob for random base
    log_matrix[log_matrix==np.inf] = 0
    #print(log_matrix)
    # print(log_matrix.shape)
    log_matrix_dict = {str(i+1): log_matrix[i] for i in range(len(log_matrix))}

    letter_pos_mapping = {"A": 0, "C": 1, "G": 2, "T": 3}

    #print(log_matrix_dict)
    all_segments = [dna_seq[start:start+12] for start in range(len(dna_seq)-11)]

    log_score_segments = []
    for segment in all_segments:
        sum = 0
        for position, letter in enumerate(segment):

            #map letter A -> position 0; C->1; G->2; T->3
            for let_map, pos_map in letter_pos_mapping.items():

                if let_map == letter:
                    sum += log_matrix_dict[str(position+1)][pos_map]

        log_score_segments.append(sum)

    return np.array(log_score_segments)





if __name__ == "__main__":

    weight_matrix = np.array([[17.7, 21.1, 29.0, 32.2],
                    [19.3, 36.1, 36.4, 8.2],           
                    [6.6, 14.8, 6.8, 71.8],
                    [83.4, 0, 0, 16.6],
                    [0, 0, 0, 100],                     
                    [95.0, 0, 0, 5],
                    [72.3, 0, 0, 27.7],
                    [94.2, 0, 5.8, 0],
                    [53.3, 0, 20.1, 26.6],
                    [29.3, 9, 51.2, 10.5],
                    [17.7, 32.5, 37.7, 12.1],
                    [22.7, 33, 33.2, 11.1]])

    # checking for spelling mistakes
    # for pos in weight_matrix:
    #     print(np.sum(pos))

    my_dna = generate_sequence(100)
    my_score = score_motifs(my_dna, weight_matrix)

    #equivalent of order() in R
    ordered = sorted(range(len(my_score)), key=lambda k: my_score[k], reverse=True)

    plt.plot([*range(len(my_score))], my_score, label="log_score")
    plt.axhline(y=0.5, color='k', linestyle='--')
    top10 = ordered[:10]
    for top in top10:
        plt.axvline(x=top, color="r", linestyle="-")
    plt.ylabel("log score")
    plt.xlabel("starting position on dna")
    plt.title("normal random DNA sequence")
    plt.show()
    # highest_log_scores = sorted(my_score, reverse=True)[:10]


# %%
#now AT-rich dna sequence
#"ATGC"
my_at_rich_dna = generate_sequence(100, [0.3, 0.3, 0.2, 0.2])
my_at_rich_score = score_motifs(my_at_rich_dna, weight_matrix)

#equivalent of order() in R
ordered_at_rich = sorted(range(len(my_at_rich_score)), key=lambda k: my_at_rich_score[k], reverse=True)

plt.plot([*range(len(my_at_rich_score))], my_at_rich_score, label="log_score")
plt.axhline(y=0.5, color='k', linestyle='--')
top10_at_rich = ordered_at_rich[:10]
for top in top10_at_rich:
    plt.axvline(x=top, color="r", linestyle="-")
plt.ylabel("log_score")
plt.xlabel("starting position on dna")
plt.title("AT-rich DNA sequence")
plt.show()  

# %%

path = r"C:\Users\aleX\Kurse\genomikI\week10\chrX_region.fna"

reads = []
for read in Bio.SeqIO.parse(path, "fasta"):
    reads.append(str(read.seq))

# print(reads)

my_score_chrX = score_motifs(reads[0], weight_matrix)

#equivalent of order() in R
ordered_chrX = sorted(range(len(my_score_chrX)), key=lambda k: my_score_chrX[k], reverse=True)

plt.plot([*range(len(my_score_chrX))], my_score_chrX, label="log_score")
plt.axhline(y=0.5, color='k', linestyle='--')
top10 = ordered_chrX[:10]
for top in top10:
    plt.axvline(x=top, color="r", linestyle="-")
plt.ylabel("log score")
plt.xlabel("starting position on dna")
plt.title("chromosome X region")
plt.show()

print("score bigger than 7: ")
bigger_seven = my_score_chrX[my_score_chrX > 7]
print(bigger_seven)
print(f"insgesamt {len(bigger_seven)} segments")

print("position: ")
index = np.array([*range(len(my_score_chrX))])
pos = index[my_score_chrX>7]
print(pos)
#print(f"insgesamt {len(pos)} segments")
#histogram
plt.hist(pos, bins=len(my_score_chrX)//100)