import pandas as pd
import os
import pyspark
from pyspark.sql import SparkSession


class InterPRO_PS:
    def __init__(self):
        if not os.path.exists("output"):
            os.makedirs("output")

    def start_SparkSession(self, host_location):
        """
        Creates sparksession at given location with given number of threads
        returns this session
        """
        spark = SparkSession.builder \
            .master(host_location) \
            .appName("Assignment5") \
            .getOrCreate()
        return spark

    def file_loader(self, ):
        """
        Loads in the tsv file and returns the data
        """

#"1. How many distinct protein annotations are found in the dataset? I.e. how many distinc InterPRO numbers are there?\n",

#"2. How many annotations does a protein have on average?\n",

#"3. What is the most common GO Term found?\n",

#"4. What is the average size of an InterPRO feature found in the dataset?\n",

#"5. What is the top 10 most common InterPRO features?\n",

#"6. If you select InterPRO features that are almost the same size (within 90-100%) as the protein itself, what is the top10 then?\n",

#"7. If you look at those features which also have textual annotation, what is the top 10 most common word found in that annotation?\n",

#"8. And the top 10 least common?\n",

#"9. Combining your answers for Q6 and Q7, what are the 10 most commons words found for the largest InterPRO features?\n",

#"10. What is the coefficient of correlation ($R^2$) between the size of the protein and the number of features found?\n",

#output should be csv with 3 columns:
    #1 question number
    #2 answer
    #3 scheduler's physical plan as string using .explain()

if __name == "__main__":
