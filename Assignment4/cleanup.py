import pandas as pd

def get_best_kmer(file):
    #takes the best kmer from the csv file
    kmer_file = pd.read_csv(file, names=["N50", "Kmer_size"], header=None)
    best_kmer = kmer_file.sort_values("N50", ascending=False).iloc[0, 1]
    return best_kmer

if __name__ == "__main__":
    best_kmer = get_best_kmer("output/output.csv")