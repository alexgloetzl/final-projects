# %%
#from extendContig import find_extension_right, extend_contig
#from makeDictionaries import make_suffix_dict, create_suffix_dicts
from readReads import read_reads
from assembleReads import assemble_reads
import Bio.SeqIO
import Bio.Seq
import random
import numpy as np


def short_read_gen(genome, n_reads_out, n_reads_out_len, name):

    gen_len = len(genome)
    random_indices = random.sample([*range(gen_len- n_reads_out_len +1)], n_reads_out)    
    reads_out = [genome[random_index:random_index+n_reads_out_len] for random_index in random_indices]

    with open(str(name)+".fna",'w',encoding = 'utf-8') as f:
        for ind, i in enumerate(reads_out):
            f.write(f">read {ind+1}\n")
            f.write(i+"\n")

    return

def faulty_short_read_gen(genome, n_reads_out, n_reads_out_len, fault, name):

    gen_len = len(genome)
    random_indices = random.sample([*range(gen_len- n_reads_out_len +1)], n_reads_out)    
    reads_out = [genome[random_index:random_index+n_reads_out_len] for random_index in random_indices]

    new_faulty_read = []
    for read in reads_out:
        for i, basepair in enumerate(read):
            if random.random() < fault:
                read = list(read)
                read[i] = random.choice(*["AGCT"])
                read = "".join(read)
                
        new_faulty_read.append(read)            

    with open(str(name)+".fna",'w',encoding = 'utf-8') as f:
        for ind, i in enumerate(new_faulty_read):
            f.write(f">read {ind+1}\n")
            f.write(i+"\n")

    return    

#%%

if __name__ == "__main__":

    #read genome fna-file
    genome = read_reads("chrM.fna", 1, verbose = False)
    #print(reads)

    #generate reads from genome
    fasta1 = short_read_gen(genome[0], 10000, 25, "fasta1")
    fasta2 = short_read_gen(genome[0], 10000, 32, "fasta2")

    #create contig
    contigs1_read = read_reads("fasta1.fna", 1.0, verbose = False)
    contigs1 = assemble_reads(contigs1_read, 5, verbose = False)
    contigs2_read = read_reads("fasta2.fna", 1.0, verbose = False)
    contigs2 = assemble_reads(contigs2_read, 5, verbose = False)


    print("contig 1 with 25 bps")
    print(len(contigs1))
    contig1_mean_len = np.mean([len(i) for i in contigs1])
    print(contig1_mean_len)
    print("contig 2 with 32 bps")
    print(len(contigs2))
    contig2_mean_len = np.mean([len(i) for i in contigs2])
    print(contig2_mean_len)

    # console output: 
    # contig 1 with 25 bps
    # 166
    # 217.74698795180723

    # contig 2 with 32 bps
    # 192
    # 197.5625

# %%

sub_samples = {}
for n in [1000, 2000, 3000, 5000]:
    my_sub = read_reads("fasta1.fna", n, verbose = False) 
    my_contig = assemble_reads(my_sub, 15, verbose = False)
    false_counter = 0
    for contig_i in my_contig:
        if genome[0].find(contig_i) == -1:
            false_counter += 1
        
    contig_mean_len = np.mean([len(i) for i in my_contig])
    sub_samples[str(n)] = [contig_mean_len,false_counter, len(my_contig)]

for key, value in sub_samples.items():
    print(f"key: {key}, mean contig length: {value[0]},\nfalse match?: {value[1]}/{value[2]}") 

#half of the generated contig do not match but those are the reverse complementary reads.
# key: 1000, mean contig length: 36.156330749354005,
# false match?: 390/774

# key: 2000, mean contig length: 57.44276094276094,
# false match?: 299/594

# key: 3000, mean contig length: 126.16176470588235,
# false match?: 140/272

# key: 5000, mean contig length: 1281.1538461538462,
# false match?: 13/26

# %%

fault_1 = faulty_short_read_gen(genome[0], 10000, 32, 0.01, "fault1")
fault1_read = read_reads("fault1.fna", 1.0, verbose = False)
#contigs1 = assemble_reads(fault1_read, 5, verbose = False)

faulty_counter = 0
for read in fault1_read:
    if genome[0].find(read) == -1:
        faulty_counter += 1

print("percent: 1%, 32 bps")
print(f"false read: {faulty_counter-len(fault1_read)/2} / {len(fault1_read)/2}")
#i would expect 3200 errors if errors are spread evenly across all reads
#maybe errors occure more than once on a read.
#those reads with two errors only count as one faulty read.

# console output:
# percent: 1%, 32 bps
# false read: 2063.0 / 10000.0

#%%

fault_01 = faulty_short_read_gen(genome[0], 10000, 32, 0.001, "fault1")
fault01_read = read_reads("fault1.fna", 1.0, verbose = False)

faulty_counter = 0
for read in fault01_read:
    if genome[0].find(read) == -1:
        faulty_counter += 1

print("percent: 0.1%, 32 bps")
print(f"false read: {faulty_counter-len(fault01_read)/2} / {len(fault01_read)/2}")

# console output:
# percent: 0.1%, 32 bps
# false read: 215.0 / 10000.0

# %%

fault_1_76 = faulty_short_read_gen(genome[0], 10000, 76, 0.01, "fault1")
fault_1_76_read = read_reads("fault1.fna", 1.0, verbose = False)

faulty_counter = 0
for read in fault_1_76_read:
    if genome[0].find(read) == -1:
        faulty_counter += 1

print("percent: 1%, 76 bps")
print(f"false read: {faulty_counter-len(fault_1_76_read)/2} / {len(fault_1_76_read)/2}")

# console output: 
# percent: 1%, 76 bps
# false read: 4325.0 / 10000.0

# --> has more faulty reads (compared to 1% 32bps) because reads are longer and errors are more likely
# within a read.
# %%

fault_01_76 = faulty_short_read_gen(genome[0], 10000, 76, 0.001, "fault1")
fault_01_76_read = read_reads("fault1.fna", 1.0, verbose = False)

faulty_counter = 0
for read in fault_01_76_read:
    if genome[0].find(read) == -1:
        faulty_counter += 1

print("percent: 0.1%, 76 bps")
print(f"false read: {faulty_counter-len(fault_01_76_read)/2} / {len(fault_01_76_read)/2}")

# console output:
# percent: 0.1%, 76 bps
# false read: 547.0 / 10000.0

# also more error prone reads

# %%

fault_01 = faulty_short_read_gen(genome[0], 10000, 32, 0.001, "fault1")
fault01_read = read_reads("fault1.fna", 1.0, verbose = False)
contigs01 = assemble_reads(fault01_read, 5, verbose = False)

faulty_counter = 0
for contig in contigs01:
    if genome[0].find(contig) == -1:
        faulty_counter += 1

print("percent: 0.1%, 32 bps")
print(f"false read: {faulty_counter-len(contigs01)/2} / {len(contigs01)/2}")
contigs01_mean_len = np.mean([len(i) for i in contigs01])
print(round(contigs01_mean_len,3))

# console output:
# percent: 0.1%, 32 bps
# false read: 253.0 / 353.0
# 76.856