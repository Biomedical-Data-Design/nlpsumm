from flair.embeddings import TransformerWordEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.data import Corpus
from flair.datasets import ColumnCorpus

# 1. get the corpus (create my corpus)
#file location
data_folder = '/home/yliu498/BERT/data_processed'

# column format indicating which columns hold the text and label(s)
columns = {0: 'text', 1: 'ner'}

corpus: Corpus = ColumnCorpus(data_folder,columns,
                              train_file = 'all_1.txt')

# 2. what label do we want to predict?
label_type = 'ner'

# 3. make the label dictionary from the corpus
label_dict = corpus.make_label_dictionary(label_type=label_type)


# 4. initialize fine-tuneable transformer embeddings WITH document context
embeddings = TransformerWordEmbeddings(model='bert-base-uncased',
                                       layers="-1",
                                       subtoken_pooling="first",
                                       fine_tune=True,
                                       use_context=True,
                                       )

# 5. initialize bare-bones sequence tagger (no CRF, no RNN, no reprojection)
tagger = SequenceTagger(hidden_size=256,
                        embeddings=embeddings,
                        tag_dictionary=label_dict,
                        tag_type=label_type,
                        use_crf=False,
                        use_rnn=False,
                        reproject_embeddings=False,
                        )
# 6. initialize trainer
trainer = ModelTrainer(tagger, corpus)

# 7. run fine-tuning
trainer.fine_tune('/home/yliu498/BERT/example-bert',
                  learning_rate=0.1,
                  mini_batch_size=32,
                  mini_batch_chunk_size=1,  # remove this parameter to speed up computation if you have a big GPU
                  max_epochs = 10)