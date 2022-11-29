
from flair.data import Corpus
from flair.datasets import ColumnCorpus

data_folder = '/home/yliu498/BERT/data_processed'

# column format indicating which columns hold the text and label(s)
columns = {0: 'text', 1: 'ner'}

corpus: Corpus = ColumnCorpus(data_folder,columns,
                              train_file = 'all_1.txt')