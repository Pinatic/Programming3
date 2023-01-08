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
    calculate percentage the feature covers on the total protein lenght

    returns:
        0 if Interpro_acc < 0.90
        1 if Interpro_acc > 0.90
    """

    if ((ddf["stop"] - ddf["start"]) / ddf["Seq_lenght"]) > 0.90:
        return 1
    else:
        return 0
