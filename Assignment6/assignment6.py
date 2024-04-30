"""Program for protein function prediction"""
import time
import pickle
import numpy as np
import dask.dataframe as dd
from dask.distributed import Client
from dask_ml import model_selection
from dask_ml.preprocessing import OneHotEncoder
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

#Starting time
start = time.time()

#path = "/data/dataprocessing/interproscan/all_bacilli.tsv"
path = "C:/Users/Pin/Desktop/Programming3/Programming3/Assignment6/bacilli_sample_1mil.tsv"

def file_loader(path, sep):
    """
    Loads in the data using the path and sep
    only loads in columns 0, 2, 6, 7, 11
    renames these columns Protein_acc, Seq_length, Start, Stop, Interpro_acc

    Arguments:
        Path:   Path to the data
        Sep:    Seperator used

    Returns:
        ddf:    Dask dataframe of the data 
    """

    ddf = dd.read_csv(path, sep = sep, usecols = [0,2,6,7,11], header = None, blocksize = "50MB",
                      names = ["Protein_acc", "Seq_length", "Start", "Stop", "Interpro_acc"])
    return ddf

def cleaner(ddf):
    """
    Removes rows containing - in collumn Interpro_acc
    drops duplicates

    Arguments:
        ddf:    Dask dataframe of the data

    Returns:
        ddf:    Dask dataframe witouth rows containing - in collumn Intrpro_acc
    """
    ddf = ddf.loc[ddf["Interpro_acc"] != "-"]
    ddf = ddf.drop_duplicates()

    return ddf

def coverage_calc(ddf):
    """
    Calculate percentage the feature covers on the total protein length
    use with .apply() method

    Arguments:
        ddf:    Dask dataframe

    Returns:
        size:   Percentage the feature covers on the protein length
     
    """
    size = (ddf["Stop"] - ddf["Start"]) / ddf["Seq_length"]
    return size

def remove_no_large_small(ddf):
    """
    Returns proteins that have a large feature (>90% of the proteins sequence)
    And that also have at least one small feature
    use with .apply() method

    Arguments:
        ddf:    Dask dataframe object grouped by protein

    Returns:
        ddf:    Dask dataframe 
    """
    if (ddf["Size"] > 0.90).any() and (ddf["Size"] < 0.90).any():
        return ddf

def group_splitter(ddf):
    """
    Takes the dataframe and splits this into two dataframes
    one dataframe containing the largests sequence per protein
    one dataframe that contains all the other sequences

    Arguments:
        ddf:    Dask dataframe

    Returns:
        ddf_large:  Dask dataframe of the largest sequence per protein
        ddf_small:  Dask dataframe of all other smaller sequences per protein
    """
    idx = ddf.groupby(["Protein_acc"])["Size"].transform(max)
    ddf_largest = ddf[idx == ddf["Size"]]
    ddf_smaller = ddf[~(ddf["Size"] == idx)]
    return ddf_largest, ddf_smaller

def merge_groups(ddf_largest, ddf_small_pivot):
    """
    Takes the dataframe containing large interpro accessions and 
        the pivoted small interpro dataframe
    merges the small interpro dataframe with the large interpro dataframe on protein

    Arguments:
        ddf_large:      Dask dataframe of largest sequence per protein
        ddf_small_piv:  Dask dataframe where columns are small interpro 
            accessions with their counts as values
    
    returns:
        dff_full:   Dask dataframe of the largest sequence per protein with 
            the count of smaller sequence that this protein also contains
    """
    ddf_full = ddf_small_pivot.merge(ddf_largest, how="inner",
                                   left_on="Protein_acc",right_on="Protein_acc")
    ddf_full = ddf_full.replace(np.nan, 0)
    ddf_full = ddf_full.reset_index()
    return ddf_full

def train_test_spliter(ddf_full):
    """
    Performs one hot encoding and train test splitting
    Arguments:
        ddf_full:       Dask dataframe with count of small interpro accessions 
            and the name of the largest protein
    
    Returns:
        X_train:        X training array
        Y_train:        Y training array
        X_test:         X testing array
        Y_test:         Y testing array
    """
    y = OneHotEncoder().fit_transform(ddf_full[["Interpro_acc"]])
    X = ddf_full.iloc[:,2:-2].to_dask_array(lengths=True).rechunk(chunk_size = "500MB")

    x_tr,x_t,y_tr,y_t = model_selection.train_test_split(X,y,random_state=24,convert_mixed_types=True)

    return x_tr, x_t, y_tr, y_t


if __name__ == "__main__":
    ddf1 = file_loader(path, "\t")
    ddf2 = cleaner(ddf1)
    ddf2["Size"] = ddf2.apply(lambda x:coverage_calc(x), axis = 1)
    #Taking only the proteins that have a large and a small interpro accession
    ddf2 = ddf2.groupby(["Protein_acc"]).apply(remove_no_large_small,
        meta={"Protein_acc":"str","Seq_length":"int64","Start":"int64",
        "Stop":"int64","Interpro_acc":"str","Size":"int64"}).reset_index(drop=True)
    ddf_large, ddf_small = group_splitter(ddf2)
    print("starting client")
    client = Client(threads_per_worker = 1, n_workers = 4, memory_limit = "4gb", dashboard_address=':8787')
    with joblib.parallel_backend("dask"):
        #Counting the number of small interpro accessions for each protein
        ddf_small = ddf_small.groupby(["Protein_acc",
                                    "Interpro_acc"])["Size"].agg("count").reset_index()
        #Pivoting the dataframe containing the small interpro accessions
        #in preperation of merging with the large accession dataframe
        ddf_small = ddf_small.categorize(columns=["Interpro_acc"])
        ddf_large = ddf_large.categorize(columns=["Interpro_acc"])
        ddf_small_piv = dd.reshape.pivot_table(ddf_small, index = "Protein_acc",
                                               columns="Interpro_acc",values="Size")
        #Merging the dataframes
        print("Merging")
        ddf_fin = merge_groups(ddf_large, ddf_small_piv)
        ddf_fin = ddf_fin.drop(columns=["Start", "Stop", "Seq_length"])
      
    client = Client(threads_per_worker = 1, n_workers = 1, memory_limit = "10gb")
    with joblib.parallel_backend("dask"):
        #Splitting the dataframe into sets
        print("Set splitting")
        X_train, X_test, y_train, y_test = train_test_spliter(ddf_fin)
        print("Sets made")

    time_past = (time.time() - start)/60
    print("Time pasted:", time_past,"Minutes", "Starting machine learning")

    client = Client(threads_per_worker = 1, n_workers = 4, memory_limit = "4gb")
    with joblib.parallel_backend("dask"):
        #Creating RandomForestClassifier
        rfc = RandomForestClassifier(random_state=0)
        #Fitting data
        rfc.fit(X_train, y_train)
        #Predicting
        y_pred = rfc.predict(X_test)
        #Accuracy score using metrics
        acc = metrics.accuracy_score(y_test, y_pred)
        #Saving model
        #filename = "/students/2021-2022/master/Pieter_DSLS/rfmodel.pkl"
        filename = "C:/Users/Pin/Desktop/Programming3/Programming3/Assignment6/rfmodel.pkl"
        pickle.dump(rfc, open(filename, "wb"))
        #Saving training data
        trainingdata= dd.from_dask_array(X_train, columns=ddf_fin.columns[2:-2])
        #trainingdata.to_csv("/students/2021-2022/master/Pieter_DSLS/trainingdata.csv")
        trainingdata.to_csv("C:/Users/Pin/Desktop/Programming3/Programming3/Assignment6/trainingdata.csv")
        print("accuracy:", acc)

    #End time
    stop = time.time()
    #duration
    duration = (stop-start)/60

    print("Total duration:", duration, "Minutes")
