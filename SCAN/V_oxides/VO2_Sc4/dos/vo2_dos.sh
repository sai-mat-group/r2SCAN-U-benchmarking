#!/bin/bash
#-------------------------
#PBS -N VO2_Sc
#PBS -l walltime=03:59:00
#PBS -q short
#PBS -k eo
#PBS -l nodes=1:ppn=64
#-------------------------

###############################################################################################################################################
#For choosing number of nodes, always choose an integral number. Currently, we have a maximum of 4 nodes in the machine
#Each node has 128 cores. Try your best to do calculations that require full nodes (i.e., all 128 cores) instead of a fraction (e.g., 64 cores)
#For example, if you need a total of 256 cores for running a 250-atom system, the following will be the PBS line
#	"#PBS -l nodes=2:ppn=128"
#
#In case your calculation really does not need even 128 cores, ask for 1 node and 64 cores as a minimum. So the PBS line would be
#	"#PBS -l nodes=1:ppn=64"
#
#If your calculation can run well within 64 cores, try to run them on the workstation or your desktop
#If your calculation requires more than 512 cores (maximum number here), Sahasrat is the only option left
#
#Available queue options for jobs are as follows
#debug (max 256 cores, max walltime 1h)
#short (max walltime 6h)
#normal (max walltime 1d)
#medium (max walltime 2d)
#long (max walltime 7d)
#
#Preliminary testing indicates NCORE = 16 is optimal
###############################################################################################################################################

#Load vasp module. Do NOT change line below
module load vasp/6.2.1

#Change into the working directory. Leave unchanged
cd $PBS_O_WORKDIR

#Below lines, except the mpirun commands, can be changed based on type of calculation done

#Job begins

#Create a temporary job directory so that the files generated by VASP are cleanly separated from the inputs
mkdir job
#Copy input files into job directory
cp INCAR KPOINTS POSCAR POTCAR CHGCAR job
#Move into job directory
cd job
#Execute vasp. Leave this line unchanged
mpirun --machinefile $PBS_NODEFILE vasp_std >& output

#Perform clean-up after calculation finishes. Remove unnecessary files (e.g., CHG, vasprun.xml, etc.)
cd ..
mv job/* .
rm -f job CHG 
bzip2 -z CHGCAR DOSCAR PROCAR vasprun.xml

#Job finished