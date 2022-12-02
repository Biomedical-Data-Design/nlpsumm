#!/bin/bash

#SBATCH --job-name=train_clinical_BERT
#SBATCH --mail-type=ALL
#SBATCH --output=/home/yliu498/BERT/script/log_file/clinical_BERT_multilabel.out
#SBATCH --mail-user=yliu498@jhu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --time=12:00:00

ml anaconda
conda activate BERT

python3 BERT_test.py

