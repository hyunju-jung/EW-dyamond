#!/bin/bash -l
#SBATCH --job-name=vert_intrpl  # Specify job name
#SBATCH --partition=compute,compute2    # Specify partition name
#SBATCH --nodes=1              # Specify number of nodes
#SBATCH --ntasks-per-node=1   # Specify number of tasks on each node
#SBATCH --time=01:00:00        # Set a limit on the total run time
#SBATCH --mail-type=FAIL       # Notify user by email in case of job failure
#SBATCH --mail-user=hyunju.jung@kit.edu # Set your e-mail
#SBATCH --account=bb1027       # Charge resources on this
#SBATCH --output=vert-%j.out    # File name for standard output
#SBATCH --error=vert-%j.err     # File name for standard error output
#SBATCH --mem=100G

module purge
module load anaconda3/bleeding_edge
source activate enstools

module list

scripts/interpolate-dyamond-vertically.py --dest /work/bb1027/m300634/prepare-dyamond/interpolated_vertical --source /work/bb1027/m300634/prepare-dyamond/interpolated_horizonatal/nwp*.nc --prefix nwp_R2B10_lkm1007_atm_3d

