#!/bin/bash
#SBATCH --time 48:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=Assignment4_pwjdejong
#SBATCH --partition=assemblix
#SBATCH --mail-type=ALL
#SBATCH --mail-user=p.w.j.de.jong@st.hanze.nl

export FILE_R1=/data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R1_001_BC24EVACXX.filt.fastq
export FILE_R2=/data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R2_001_BC24EVACXX.filt.fastq
export OUTPUT=/students/2021-2022/master/Pieter_DSLS/output

mkdir -p /students/2021-2022/master/Pieter_DSLS/output
mkdir -p output

#run velveth and velvetg

seq 20 2 30 | parallel -j16 'velveth $OUTPUT/{} {} -longPaired -fastq $FILE_R1 $FILE_R2 && velvetg $OUTPUT/{} && cat &OUTPUT/{}/contigs.fa | (python3 assignment4.py && echo -e {}; ) >> output/output.csv'

#run the cleanup

python3 cleanup.py

#clear the no longer needed files

rm -rf $OUTPUT