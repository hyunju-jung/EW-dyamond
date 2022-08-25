#!/bin/bash -l
#SBATCH --job-name=create_weights  # Specify job name
#SBATCH --partition=compute,compute2    # Specify partition name
#SBATCH --nodes=1              # Specify number of nodes
#SBATCH --ntasks-per-node=1   # Specify number of tasks on each node
#SBATCH --time=01:00:00        # Set a limit on the total run time
#SBATCH --mail-type=FAIL       # Notify user by email in case of job failure
#SBATCH --mail-user=hyunju.jung@kit.edu # Set your e-mail
#SBATCH --account=bb1027       # Charge resources on this
#SBATCH --output=weights-%j.out    # File name for standard output
#SBATCH --error=weights-%j.err     # File name for standard error output
#SBATCH --mem=100G

module purge
module load anaconda3/bleeding_edge
source activate enstools

module list
which python3
which activate

env

/home/mpim/m300634/conda-envs/enstools/bin/python3 scripts/interpolate-dyamond-horizontally.py --grid /pool/data/ICON/grids/public/mpim/0017/icon_grid_0017_R02B10_G.nc --source /work/ka1081/DYAMOND/ICON-2.5km/nwp_R2B10_lkm1007_atm_3d_pres_ml_20160801T000000Z.grb --dest /work/bb1027/m300634/prepare-dyamond/interpolated_horizonatal --weights /work/bb1027/m300634/prepare-dyamond/weights.pkl
