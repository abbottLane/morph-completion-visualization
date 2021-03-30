import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import os
import pandas as pd

DATA_DIR = 'data/tsv/real-words.tsv'

def main():
   build_uniqueness_plot("WordSample",load_tsv(DATA_DIR))

def load_tsv(filepath):
    return pd.read_csv(filepath,index_col=None,sep='\t')

def build_uniqueness_plot(name, data):
    cmap = sns.cubehelix_palette(dark=.3, light=.8, as_cmap=True)

    print(data.head())
    print("space")
    print(data.min())
    #ax = sns.catplot(x="x", y="y", jitter=True,data=data)
    g = sns.catplot(x="x", y="y", kind="boxen", k_depth="full",
            data=data)
    ax = plt.axhline(100, ls='--', color='g', label="100")
    ax = plt.axhline(50, ls='--', color='r')
    ax = plt.axhline(25, ls='--', color='b')
    
    plt.annotate('50', xy=(3, 1),  xycoords='data',
            xytext=(0.005, 0.44), textcoords='axes fraction',
            )
    plt.annotate('25', xy=(3, 1),  xycoords='data',
            xytext=(0.005, 0.37), textcoords='axes fraction',
            )
    g.set(yscale="log")
    # plt.text(0.9,25, "Some text")
    g.set_axis_labels("Number of Input Characters ", "Number of Possible Completions")
    g.set(ylim=(1,9500))
    #ax.set(xlabel='Number of Characters in Input', ylabel='Number of Possible Completions', title= name + " Prefix Completions")
    plt.show()

if __name__=="__main__":
    main()