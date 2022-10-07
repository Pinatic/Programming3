#!/bin/bash
#SBATCH --time 5:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=Assignment3_pwjdejong
#SBATCH --partition=assemblix
#SBATCH --mail-type=ALL
#SBATCH --mail-user=p.w.j.de.jong@st.hanze.nl

export FILE_R1=/data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R1_001_BC24EVACXX.filt.fastq
export FILE_R2=/data/dataprocessing/MinIONData/MG5267/MG5267_TGACCA_L008_R2_001_BC24EVACXX.filt.fastq
export OUTPUT=/students/2021-2022/master/Pieter_DSLS/output

mkdir -p /students/2021-2022/master/Pieter_DSLS/output
mkdir -p output

#run velveth and velvetg

parallel -j 16 "velveth $OUTPUT/{} {} -fastq -longPaired $FILE_R1 $FILE_R2 && velvetg $OUTPUT/
