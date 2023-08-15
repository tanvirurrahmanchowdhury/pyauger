#!/bin/bash -l

# Name of the job
#SBATCH --job-name=cluster-jobs-insb

# Number of cores, in this case one
#SBATCH --cpus-per-task=64

# Walltime (job duration)
#SBATCH --time=48:00:00

# Email
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f006nd7@dartmouth.edu

#SBATCH --partition=preemptable

module load intel-compilers/18.1
module load mpich/3.2.1-intel18.1
module load mkl/18.1

INCR=INCAR
KPTS=KPOINTS
PTCR=POTCAR
PSCR=POSCAR
WV=CHGCAR
CALC_PARAM="k_grid_"
kpoints=( 10 20 50 100 )

# Run Calculation
for VAR in "${kpoints[@]}"; do
  if [ ! -d $CALC_PARAM$VAR ]; then mkdir $CALC_PARAM$VAR; fi
  
  # Copy files
  if [ -d $CALC_PARAM$VAR ]; then
  cp $INCR $CALC_PARAM$VAR/INCAR
  cp $PTCR $CALC_PARAM$VAR/POTCAR
  cp $KPTS $CALC_PARAM$VAR/KPOINTS
  cp $PSCR $CALC_PARAM$VAR/POSCAR
  cp $WV $CALC_PARAM$VAR/CHGCAR
  
  # Edit INCAR/KPOINTS/POSCAR. Comment any lines don't needed
  #sed -i "s/.*.*/AEXX = $VAR/" $CALC_PARAM$VAR/INCAR
  sed -i "4s/.* .*/$VAR $VAR $VAR/" $CALC_PARAM$VAR/KPOINTS
  #sed -i "2s/.*/$VAR/" $CALC_PARAM$VAR/POSCAR
  # Run VASP
  cd $CALC_PARAM$VAR; mpirun -n 64 vasp_std > vasp.out; cd ../
  
  fi
  
done
