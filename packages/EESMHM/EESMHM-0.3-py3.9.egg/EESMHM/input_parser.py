import os
from .AminoAcidConverter import *

def inputParser(input_file):
    positions_and_mutations = {}
    if os.path.exists(input_file):
        with open(input_file, "r") as infile:
            for line in infile.readlines():
                wt_aa, position, mutations = line.split()
                if len(mutations) == 1:
                    if mutations == "*":
                        mutations = [i for i in all_aa_one() if i != wt_aa ]
                    else:
                        mutations = list(mutations)
                else:
                    mutations = mutations.split(",")
                positions_and_mutations[one_to_three(wt_aa)+ "_" +position] = mutations
    return positions_and_mutations
