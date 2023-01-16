import pandas as pd
import numpy as np
import dask.dataframe as dd
import dask.array as da
import time
import pickle

start = time.time()

#path = "/data/dataprocessing/interproscan/all_bacilli.tsv"

def file_loader(self, path, sep):
    """
    Loads in the data using the path and sep
    only loads in columns 0, 2, 6, 7, 11
    renames these columns Protein_acc, Seq_lenght, Start, Stop, Interpro_acc

    returns dask dataframe
    """

    ddf = dd.read_csv(path, sep, usecols = [0,2,6,7,11], names = ["Protein_acc", "Seq_lenght", "Start", "Stop", "Interpro_acc"])
    
    return ddf

def cleaner(self, ddf):
    """
    removes rows containing - in collumn Interpro_acc
    drops duplicates

    returns dask dataframe
    """
    ddf = ddf[ddf["Interpro_acc"] != "-"]
    ddf = ddf.drop_duplicates()

    return ddf

def coverage_calc(ddf):
    """
    calculate percentage the feature covers on the total protein length
    use with .apply() method

    returns percentage the feature covers on the protein length
     
    """
    
    Size = (ddf["Stop"] - ddf["Start"]) / ddf["Seq_lenght"]
    return Size

def 



if __name__ == "__main__":
    ddf = file_loader(path, "\t")
    ddf = cleaner(ddf)
    ddf["Size"] = ddf.apply(lambda x:coverage_calc(x), axis = 1)


