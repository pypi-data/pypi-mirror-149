import urllib.request
import os
import argparse
import sys
from pericaat.pdb_fixinsert import fixInsert

def CLI():
    files = [i for i in os.listdir() if i.endswith(".pdb")]
    parser = argparse.ArgumentParser()
    parser.add_argument('-pdb',
                        help=f"please choose an input file from {files}", default=None)
    parser.add_argument('-qc', '--query_chain', help="please choose a query chain", default=None)
    parser.add_argument('-ic', '--interacting_chain',
                        help="please choose the interacting chain", default=None)
    parser.add_argument('-sr', '--solvent_radius',
                        help="please choose the solvent radius extention (defualt 2.4)", default=2.4)
    parser.add_argument('-r', '--result_file',
                        help="result file", default="result.txt")
    parser.add_argument(
        '-mi', '--min_ints', help="please choose the minimum interaction (defualt 1)", default=1)
    parser.add_argument(
        '-s', '--scwrl', help="use Scrwl4 to remodel sidechains", action= 'store_true', default=False)
    parser.add_argument(
        '-m', '--mutants', help="mutants to change to: ex TRP,ARG", default="TRP,ARG")
    parser.add_argument(
        '-qh', '--qhull', help="use c++ qhull", action= 'store_true', default=False)
    parser.add_argument(
        '-p', '--parallel', help="run program in parrel", action= 'store_false', default=True)
    parser.add_argument(
        '-nomod', '--nomodeller', help="do not use modeller", action= 'store_true', default=False)
    parser.add_argument(
        '-c', '--cores', help="number of pareller jobs to run at once", default=4)
    args = parser.parse_args()
    pdb = args.pdb
    partner_chain = args.interacting_chain
    query_chain = args.query_chain
    sr = args.solvent_radius
    result_file = args.result_file
    mi = args.min_ints
    scwrl = args.scwrl
    nomod = args.nomodeller
    qhull = args.qhull
    parallel = args.parallel
    cores = int(args.cores)
    mutants = args.mutants
    mutants = mutants.split(",")
    mutants = [i.upper() for i in mutants]
    for i in mutants:
        if len(i) != 3:
            print("Error please use three letter amino acid code separated by a comma")
            sys.exit()
    if mi > 4:
        print("Error please choose `mi` less than 4")
        sys.exit()
    pdb, pdb_file = pdbManager(pdb, files)
    if query_chain is None or partner_chain is None:
        query_chain, partner_chain, pdb_file = getChains(pdb_file)
    else:
        query_chain = query_chain[0]
        partner_chain = partner_chain[0]
        pdb_file = fixInsert(pdb_file)
    os.makedirs("output/", exist_ok=True)
    os.makedirs(f"output/{pdb}/mutants/", exist_ok=True)
    return pdb, pdb_file, query_chain, partner_chain, sr, result_file, mi, scwrl, mutants, qhull,nomod, cores, parallel


def pdbManager(pdb, files):
    if pdb is None:
        pdb = input("Please input a pdb id (ex. 1i8l): ")
        pdb = pdb.lower()
    if not pdb.endswith(".pdb"):
        pdb_file = pdb + ".pdb" 
    else:
        pdb_file = pdb
        pdb = pdb.replace(".pdb", "")
    if pdb_file not in files:
        download = input(f"Download {pdb} from the RCSB? [y,n]: ")
        if download == "y":
            download_pdb(pdb, "")
        else:
            print(f"{pdb} not downloaded please add {pdb} to input folder")
            sys.exit()
    return pdb, pdb_file
        

def download_pdb(pdbcode, datadir, downloadurl="https://files.rcsb.org/download/"):
    """
    Downloads a PDB file from the Internet and saves it in a data directory.
    :param pdbcode: The standard PDB ID e.g. '3ICB' or '3icb'
    :param datadir: The directory where the downloaded file will be saved
    :param downloadurl: The base PDB download URL, cf.
        `https://www.rcsb.org/pages/download/http#structures` for details
    :return: the full path to the downloaded PDB file or None if something went wrong
    """
    pdbfn = pdbcode + ".pdb"
    url = downloadurl + pdbfn
    outfnm = os.path.join(datadir, pdbfn)
    try:
        urllib.request.urlretrieve(url, outfnm)
        return outfnm
    except Exception as err:
        print(str(err), file=sys.stderr)
        return None


def getChains(pdb_file):
    chains = set()
    has_icode = False
    with open(f"{pdb_file}", "r") as pdb_fh:
        for line in pdb_fh:
            if line.startswith("ATOM"):
                chains.add(line[21])
                if line[26] != ' ':
                    has_icode = True
    qc = input(f"Please select query [{chains}]: ")
    if qc not in chains:
        print("chain not found")
        sys.exit()

    chains.remove(qc)
    ic = input(f"Please select interacting chain [{chains}]: ")
    if ic not in chains:
        print("chain not found")
        sys.exit()
    if has_icode:
        pdb_file = fixInsert(pdb_file)
    return qc, ic ,pdb_file
