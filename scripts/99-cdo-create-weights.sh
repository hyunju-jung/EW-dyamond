#!/bin/bash -l
#SBATCH --job-name=horz_intrpl  # Specify job name
#SBATCH --partition=shared    # Specify partition name
#SBATCH --nodes=1              # Specify number of nodes
#SBATCH --ntasks-per-node=1   # Specify number of tasks on each node
#SBATCH --time=02:00:00        # Set a limit on the total run time
#SBATCH --mail-type=FAIL       # Notify user by email in case of job failure
#SBATCH --mail-user=hyunju.jung@kit.edu # Set your e-mail
#SBATCH --account=bb1163       # Charge resources on this
#SBATCH --output=test-%j.out    # File name for standard output
#SBATCH --error=test-%j.err     # File name for standard error output
#SBATCH --mem=100G
#SBATCH --array=0-0          # index 0 is skipped when the file is already used in script 01--

module purge
module load cdo

opath="/work/bk1040/DYAMOND/data/summer_data/"
odir="ICON-80km"
grid_file="icon_grid_0019_R02B05_G.nc" #"icon_grid"

files=(`ls ${opath}${odir}/nwp_*_atm2_2d_ml_*.grb | sort`)

cdo -f nc gencon,grid_des_2.5x2.5 -setgrid,${opath}${odir}/${grid_file} ${files[$SLURM_ARRAY_TASK_ID]} ${odir}/weights_2.5x2.5.nc

sbatch 99-cdo-remapping.sh ${odir} ${grid_file}
