import pandas as pd
import numpy as np
import dask.dataframe as dd
import dask.array as da
from dask.distributed import Client
import time
import pickle
import joblib

#Starting time
start = time.time()

#path = "/data/dataprocessing/interproscan/all_bacilli.tsv"

def file_loader(path, sep):
    """
    Loads in the data using the path and sep
    only loads in columns 0, 2, 6, 7, 11
    renames these columns Protein_acc, Seq_lenght, Start, Stop, Interpro_acc

    returns dask dataframe
    """

    ddf = dd.read_csv(path, sep, usecols = [0,2,6,7,11], names = ["Protein_acc", "Seq_lenght", "Start", "Stop", "Interpro_acc"])
    
    return ddf

def cleaner(ddf):
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

def remove_no_large_small(ddf):
    """
    Returns proteins that have a large feature (>90% of the proteins sequence)
    And that also have at least one small feature
    use with .apply() method

    returns dask dataframe 
    """
    if (ddf["Size"] > 0.90).any() and (ddf["Size"] < 0.90).any():
        return ddf

def group_splitter(ddf):
    """
    Takes the dataframe and splits this into two dataframes
    one dataframe containing the largests sequence per protein
    one dataframe that contains all the other sequences

    returns:
        ddf_large
        ddf_small
    """
    idx = ddf.groupby(["Protein_acc"])["Size"].transform(max)
    ddf_large = ddf[idx == ddf["Size"]]
    ddf_small = ddf[~(idx == ddf["Size"])]
    return ddf_large, ddf_small


def merge_groups(ddf_large, ddf_small):
    """
    
    """

if __name__ == "__main__":
    ddf = file_loader(path, "\t")
    ddf = cleaner(ddf)
    ddf["Size"] = ddf.apply(lambda x:coverage_calc(x), axis = 1)
    #Taking only the proteins that have a large and a small interpro accession
    ddf = ddf.groupby(["Protein_acc"]).apply(remove_no_large_small).reset_index(drop = True)
    ddf_large, ddf_small = group_splitter(ddf)
    
    client = Client()
    with joblib.parallel_backend("dask"):

        ddf_small_piv = dd.reshape.pivot_table(ddf_small, index="Protein_acc", columns="Interpro_acc", values="Size")

