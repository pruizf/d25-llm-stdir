#!/bin/sh

#echo "remove the constraint to use large gpus if not needed else comment this line" && exit

#SBATCH -p publicgpu
#SBATCH -N 1
#SBATCH -A lilpa
#SBATCH --gres=gpu:1
##SBATCH --constraint="gpup100|gpuv100|gpurtx5000|gpua100"

# llama_client.py batch_name corpus_name
# batch_name starts with 'batch_'
# e.g run_llama.sh batch_007 data/stgdir_labelGeneric_trainvalid_100-test_30.csv
time python3 llama_client.py $1 $2