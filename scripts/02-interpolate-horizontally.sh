#!/bin/bash -l
#SBATCH --job-name=horz_intrpl  # Specify job name
#SBATCH --partition=compute,compute2    # Specify partition name
#SBATCH --nodes=1              # Specify number of nodes
#SBATCH --ntasks-per-node=1   # Specify number of tasks on each node
#SBATCH --time=02:00:00        # Set a limit on the total run time
#SBATCH --mail-type=FAIL       # Notify user by email in case of job failure
#SBATCH --mail-user=hyunju.jung@kit.edu # Set your e-mail
#SBATCH --account=bb1027       # Charge resources on this
#SBATCH --output=horz-%j.out    # File name for standard output
#SBATCH --error=horz-%j.err     # File name for standard error output
#SBATCH --mem=100G
#SBATCH --array=1-125           # index 0 is skipped because the file is already used in script 01--

module purge
module load anaconda3/bleeding_edge
module list
source activate enstools

#files=(`ls /work/ka1081/DYAMOND/ICON-2.5km/*3d_pres_ml* /work/ka1081/DYAMOND/ICON-2.5km/*3d_u_ml* /work/ka1081/DYAMOND/ICON-2.5km/*3d_v_ml* | sort`)
<<<<<<< HEAD
files=(`ls /work/ka1081/DYAMOND/ICON-2.5km/*3d_t_ml* /work/ka1081/DYAMOND/ICON-2.5km/*3d_qv_ml* | sort`)
=======
files=(`ls /work/ka1081/DYAMOND/ICON-2.5km/nwp_R2B10_lkm1007_atm2_2d_ml_*.grb | sort`)

odir="/work/bb1027/m300634/prepare-dyamond/interpolated_horizontal"
>>>>>>> 0b495c988f64690a2facb28b2a86ba278bcec50d

echo ${files[$SLURM_ARRAY_TASK_ID]}

/home/mpim/m300634/conda-envs/enstools/bin/python3 scripts/interpolate-dyamond-horizontally.py --grid /pool/data/ICON/grids/public/mpim/0017/icon_grid_0017_R02B10_G.nc --source ${files[$SLURM_ARRAY_TASK_ID]} --dest $odir --weights /work/bb1027/m300634/weights.pkl

