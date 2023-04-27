#!/bin/bash

#SBATCH --job-name=train_BERT
#SBATCH --mail-type=ALL
#SBATCH --mail-user=yliu498@jhu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --time=12:00:00

ml anaconda
conda activate BERT

python3 BERT_test.py

