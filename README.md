# morph-completion-visualization
Scripts to generate morph completion visualizations, as seen in "Interactive Word Completion for Morphologically Complex Languages"

## Usage
Requirements:
-`pip install seaborn`

There are two main scripts here:
- `words2tsv.py` lets you define your FSTs, a pointer to a list of words, and a pointer to where you want to write the processed tsv file. The output of this process is what is visualized by the second script.
- `visualize_morph_data.py` points to a processed tsv file generated b the script above, and visualizes it as a boxen plot with seaborn. 