#bash script that saves timings from using 1 till 16 threads

export BLASTDB=/local-fs/datasets/

mkdir -p output

for n in {1..16} ; do /usr/bin/time -o timings.txt --append -f "${n}\t%e" blastp -query MCRA.faa -db refseq_protein/refseq_protein -num_threads $n -outfmt 6 >> blastoutput.txt ; done

python3 Assignment3.py