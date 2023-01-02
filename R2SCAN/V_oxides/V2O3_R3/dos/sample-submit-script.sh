#!/bin/bash
#SBATCH --job-name=V2O3_R    			# Job name
#SBATCH --export=ALL				# Export environment variables
#SBATCH --qos=normal				# See qos documentation below
#SBATCH --nodes=1                   		# Run on a single node (only 1 available on this machine)
#SBATCH --ntasks=24                   		# Max number of tasks. Ask for either 24 or 48.
#SBATCH --no-requeue				# Don't requeue job unneccessarily
#SBATCH --time=23:59:00               		# Time limit hrs:min:sec
#SBATCH --output=job_%j.log   			# Standard output from SLURM and error log

####################################
#Available QOS options are
#debug: < 1hr jobs
#short: < 6hr jobs
#normal: < 1day jobs
#medium: < 2day jobs
#long: < 1week jobs
#Jobs whose walltimes don't match with appropriate QoS will be rejected by the queuing system
#Default qos is normal (if left unspecified in the header SBATCH command above)
####################################

#Load correct version of VASP
module load vasp/6.2.1

#Ensure "srun" can function with MPI below. This line will not need modification
export I_MPI_PMI_LIBRARY=/usr/lib/x86_64-linux-gnu/libpmi.so.0

#Job begins
echo "Job started at $(date)"

#Modify lines below as necessary to run a job
srun vasp_std >& output

#Job ends
echo "Job finished at $(date)"
