#!/bin/bash
#SBATCH --time 5:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=Assignment3_pwjdejong
#SBATCH --partition=assemblix
#SBATCH --mail-type=ALL
#SBATCH --mail-user=p.w.j.de.jong@st.hanze.nl

export BLASTDB=/local-fs/datasets/

mkdir -p output

for n in {1..16}; do /usr/bin/time -o output/timings.txt --append -f "${n}:%e" blastp -query MCRA.faa -db refseq_protein/refseq_protein -num_threads $n -outfmt 6 >> blastoutput.txt; done

python3 assignment3.py
