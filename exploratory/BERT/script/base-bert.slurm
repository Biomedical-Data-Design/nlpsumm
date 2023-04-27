#!/bin/bash

#SBATCH --job-name=train_base-bert
#SBATCH --mail-type=ALL
#SBATCH --output=/home/yliu498/BERT/script/log_file/base-bert.out
#SBATCH --mail-user=yliu498@jhu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --time=6:00:00

ml anaconda
conda activate BERT

python3 base-bert.py