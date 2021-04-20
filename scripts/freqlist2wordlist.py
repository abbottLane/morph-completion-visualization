"""The purpose of this script is to convert the cree "words by frequency" 
txt file into a simple word list for the visualization script.
"""
import re

INDIR = "/home/wlane/projects/morph-completion-visualization/data/words/cree_words_by_freq.txt"
OUTDIR = "/home/wlane/projects/morph-completion-visualization/data/words/cree_wordlist.txt"

def main():
    lines = []
    with open(INDIR, "r") as f:
        lines = f.readlines()
        lines = [x.split()[1] for x in lines]
    
    with open(OUTDIR, "w") as g:
        for l in lines:
            l = re.sub("-", "", l)
            g.write(l.lower() + "\n")




if __name__ == "__main__":
    main()