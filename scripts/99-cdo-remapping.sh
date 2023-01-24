#!/bin/bash -l
#SBATCH --job-name=horz_intrpl  # Specify job name
#SBATCH --partition=shared #compute    # Specify partition name
#SBATCH --nodes=1              # Specify number of nodes
#SBATCH --ntasks-per-node=1   # Specify number of tasks on each node
#SBATCH --time=02:00:00        # Set a limit on the total run time
#SBATCH --mail-type=FAIL       # Notify user by email in case of job failure
#SBATCH --mail-user=hyunju.jung@kit.edu # Set your e-mail
#SBATCH --account=bb1163       # Charge resources on this
#SBATCH --output=remap-share-%j.out    # File name for standard output
#SBATCH --error=remap-share-%j.err     # File name for standard error output
#SBATCH --mem=100G
#SBATCH --array=0-40 #0-40          # index 0 is skipped when the file is already used in script 01--

module purge
module load cdo

opath="/work/bk1040/DYAMOND/data/summer_data/"
#odir="ICON-10km"
#grid_file="icon_grid_0025_R02B08_G.nc"
odir=$1
grid_file=$2

echo ${odir}
echo ${grid_file}

files=(`ls ${opath}${odir}/*_atm2_2d_ml_*.grb | sort`)

mstring=$(printf %04d $SLURM_ARRAY_TASK_ID)

echo $mstring
echo ${files[$SLURM_ARRAY_TASK_ID]}
cdo -P 8 -f nc -remap,grid_des_2.5x2.5,${odir}/weights_2.5x2.5.nc -selname,tp ${files[$SLURM_ARRAY_TASK_ID]} ${odir}/nwp_atm2_2d_ml_${mstring}.nc