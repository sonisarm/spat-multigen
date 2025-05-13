# Script: parallel_structure.slurm # 

#!/bin/bash
#SBATCH -J structure
#SBATCH -t 5-00:00:00
#SBATCH -n 15
#SBATCH -N 1
#SBATCH --mem 32G
#SBATCH -e assembly_%j.err
#SBATCH -o assembly_%j.out
#SBATCH -p q1

# NOTA: Lanzar el arreglo de la siguiente manera:
# sbatch --array=1-10%3 parallel_structure.slurm

# Cargar los módulos requeridos para q1:
module load structure/2.3.4/gcc/9.3.0-h4nj \
        structureharvester/1.0/gcc/9.3.0-b5ct \
        parallel/20190222/gcc/9.3.0-734l

# seq 10 | parallel: para lanzar 10 procesos en paralelo (del 1 al 10)
# la primer variable posicional es para K=SLURM_ARRAY_TASK_ID
# la seguna variable posicional es para el número de repetición (entre 1 y 10)

seq 30 | parallel ./structure.sh ${SLURM_ARRAY_TASK_ID} {}


# Script: structure.slurm # 
#!/bin/bash
#SBATCH -J structure
#SBATCH -t 5-00:00:00
#SBATCH -n 15
#SBATCH -N 1
#SBATCH --mem 32G
#SBATCH -e assembly_%j.err
#SBATCH -o assembly_%j.out
#SBATCH -p q1

# NOTA: Lanzar el arreglo de la siguiente manera:
# sbatch --array=1-10%3 parallel_structure.slurm

# Cargar los módulos requeridos para q1:
module load structure/2.3.4/gcc/9.3.0-h4nj \
        structureharvester/1.0/gcc/9.3.0-b5ct \
        parallel/20190222/gcc/9.3.0-734l

# seq 10 | parallel: para lanzar 10 procesos en paralelo (del 1 al 10)
# la primer variable posicional es para K=SLURM_ARRAY_TASK_ID
# la seguna variable posicional es para el número de repetición (entre 1 y 10)

seq 30 | parallel ./structure.sh ${SLURM_ARRAY_TASK_ID} {}

[ssarmiento@login1 interisland]$ cat structure.sh
#!/bin/bash

K=$1
REP=$2

OUTNAME="Species_K${1}_${2}"

structure -K ${1} \
              -o ${OUTNAME} \
              -i Species \
              -m mainparams.txt \
              -e extraparams.txt \


# Command to run: sbatch --array=1-11%3 parallel_structure.slurm