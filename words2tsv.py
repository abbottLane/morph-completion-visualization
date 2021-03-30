from foma import FST
import csv
from random import randint
fst = FST.load('grammars/kunwok.fsm')
autocomplete = FST.load('grammars/autocomplete.fsm')


WORDS = 'data/words/actual-words-gup.txt'
TSV_OUT = 'data/tsv/real-words.tsv'

def main():
    lexicon = load_vocab(WORDS)
    prefix_lexicon = get_prefix_dict(lexicon)
    build_tsv(prefix_lexicon)
    

def build_tsv(prefix_lexicon):
    rows = [["x","y","name"]]
    for order, preflist in prefix_lexicon.items():
        print("Reached order: " + str(order))
        if order != 0:
            for pref in preflist:
                results = autocomplete.apply_down(pref)
                results = list(set([x for x in results if "Guess" not in x])) # if "Guess" not in x]
                rows.append([order, len(results), pref])
    
    with open(TSV_OUT, "w") as f:
        tsv_writer = csv.writer(f, delimiter="\t")
        for r in rows:
            tsv_writer.writerow(r)
        
def change_one_char(word):
    return word[:-1] + "x"
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

    return deduped


def load_vocab(filepath):
    lines = []
    with open(filepath, "r") as f:
        return [x.strip() for x in list(set(f.readlines()))]

if __name__=="__main__":
    main()