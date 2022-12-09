#!/bin/bash

#SBATCH --job-name=train_roberta-large
#SBATCH --mail-type=ALL
#SBATCH --output=/home/yliu498/BERT/script/log_file/roberta-large.out
#SBATCH --mail-user=yliu498@jhu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --time=6:00:00

ml anaconda
conda activate BERT

python3 roberta-large.py