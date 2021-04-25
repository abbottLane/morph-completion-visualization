import hfst
import csv
import ast
from random import randint
import subprocess
import multiprocessing as mp

# hfst_process = hfst.HfstInputStream('grammars/crk-infl-morpheme-completion.hfstol')
# my_hfst = hfst_process.read()

MODEL = "grammars/crk-infl-morpheme-completion.hfstol"
WORDS = '/home/wlane/projects/morph-completion-visualization/data/words/cree_wordlist.txt'
TSV_OUT = '/home/wlane/projects/morph-completion-visualization/data/tsv/cree-wordlist.tsv'

def main():
    lexicon = load_vocab(WORDS)
    prefix_lexicon = get_prefix_dict(lexicon)
    build_tsv(prefix_lexicon)
    

def build_tsv(prefix_lexicon):
    rows = [["x","y","name"]]
    
    for order, preflist in prefix_lexicon.items():
        print("Reached order: " + str(order))
        if order != 0:
                pool = mp.Pool(mp.cpu_count())
                results=[pool.apply_async(invoke_fst_subprocess, args=(pref,order)) for pref in preflist]
                pool.close()
                rows.extend([x.get() for x in results])
    
    with open(TSV_OUT, "w") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        for r in rows:
            tsv_writer.writerow(r)

def invoke_fst_subprocess(pref, order):
    results = subprocess.run(
                    ["hfst-optimized-lookup", "-q", "-u", MODEL],
                    input=pref.encode('utf-8'),
                    stdout=subprocess.PIPE
                    )
    results = str(results.stdout.decode('utf-8')).split("\n")
    results = [x for x in results if " " not in x] # filter out the full-phrase completions
    return [order, len(results)-1, pref]

def get_prefix_dict(lexicon):
    lexicon = sorted(lexicon, key=len)
    longest_len = len(lexicon[-1])

    prefix_dict = {}
    for order in range(longest_len):
        prefix_dict[order] = []
        for word in lexicon:
            if order <= len(word):
                prefix_dict[order].append(word[:order])
    
    # dedupe
    deduped = {}
    for k,v in prefix_dict.items():
        deduped[k] = list(set(v))

    for k,v in deduped.items():
        print("Key: " + str(k) + "\t" + "Value_len: " + str(len(v))) # so we can see shape of computational load
    return deduped


def load_vocab(filepath):
    lines = []
    with open(filepath, "r") as f:
        return [x.strip() for x in list(set(f.readlines()))]

if __name__=="__main__":
    main()