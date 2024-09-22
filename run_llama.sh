#!/bin/sh

#echo "remove the constraint to use large gpus if not needed else comment this line" && exit

#SBATCH -p publicgpu
#SBATCH -N 1
#SBATCH -A lilpa
##SBATCH --gres=gpu:1
##SBATCH --constraint="gpup100|gpuv100|gpurtx5000|gpua100"
#SBATCH --constraint="gpup100|gpuv100|gpurtx5000|gpurtx6000|gpua100"

# Usage: llama_client.py batch_name corpus_name model_name
#   - batch_name starts with 'batch_'
#   - possible model names are in config.py
#   - Example: run_llama.sh batch_007 data/stgdir_labelGeneric_trainvalid_100-test_30.csv llama-3.1

# try to run python with -u (unbuffered) to see print messages on slurm log as they are issued
# (otherwise they will be buffered and printed at the end of the job)

time python3 -u llama_client.py $1 $2 $3
