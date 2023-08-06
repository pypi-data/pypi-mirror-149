import os
import sys

"""
Adapted from https://github.com/haddocking/pdb-tools
"""

def simple_mutate(pdb, qc, respos, wt_res,mutAA, mutantfile):
    mutated_structure = []
    mutposition = mutAA + str(respos)
    with open(f"{pdb}", "r") as _pdbfh:
        for line in _pdbfh:
            if line[0:4] == 'ATOM' or line[0:6] == 'HETATM':
                s_chain = line[21].strip()
                s_resi = line[22:26].strip()
                s_resn = line[17:20].strip()
                if s_chain == qc and s_resi == respos:
                    if s_resn == wt_res:
                        line = line[0:17]+mutAA+line[20:]
                        mutated_structure.append(line)
                    else:
                        print("Error:")
                        return None
                else:
                    mutated_structure.append(line)
            else:
                mutated_structure.append(line)
    with open(mutantfile, "w+") as _mutfile:
        for line in mutated_structure:
            _mutfile.write(line)
    return mutantfile

