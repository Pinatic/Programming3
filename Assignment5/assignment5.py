from ast import In
import pandas as pd
import os
import pyspark
from pyspark.sql import SparkSession


class InterPRO_PS:
    def __init__(self):
        if not os.path.exists("output"):
            os.makedirs("output")

    def start_sparksession(self, host_location):
        """
        Creates sparksession at given location with given number of threads
        returns this session
        """
        spark = SparkSession.builder \
            .master(host_location) \
            .appName("Assignment5") \
            .getOrCreate()
        return spark

    def file_loader(self, path, sep, pyspark_obj):
        """
        Loads in the tsv file and returns the data
        .tsv uses /t dilimiter
        """
        data = pyspark_obj.read.option("sep", sep).csv(path)
        return data
    
    def get_questions(self, df):
        
        #1. How many distinct protein annotations are found in the dataset? I.e. how many distinc InterPRO numbers are there?
        Q1_explain = df.select("_c11").filter(df._c11 != "-").distinct()._jdf.queryExecution().toString()
        Q1_answer = df.select("_c11").filter(df._c11 != "-").distinct().count()

        #2. How many annotations does a protein have on average?
        Q2_explain = df.select("_c11").filter(df._c11 != "-").distinct()._jdf.queryExecution().toString()
        Q2_answer = df.select("_c11").filter(df._c11 != "-").count() / df.select("_c11").filter(df._c11 != "-").distinct().count()

        #3. What is the most common GO Term found?
        Q3_explain = df.withColumn("_c13", explode(split(col("_c13"), "\\|"))).select("_c13").filter(df._c13 != "-").agg({"_c13": "max"})._jdf.queryExecution().toString()
        Q3_answer = df.withColumn("_c13", explode(split(col("_c13"), "\\|"))).select("_c13").filter(df._c13 != "-").agg({"_c13": "max"}).collect()[0][0]

        #4. What is the average size of an InterPRO feature found in the dataset?
        Q4_explain = df.select(abs(df._c7 - df._c8)).agg({"abs((_c7 - _c8" : "mean"})._jdf.queryExecution().toString()
        Q4_answer = df.select(abs(df._c7 - df._c8)).agg({"abs((_c7 - _c8" : "mean"}).collect()[0][0]

        #5. What is the top 10 most common InterPRO features?
        Q5_explain = df.filter(df._c11 != "-").groupBy("_c11").count()._jdf.queryExecution().toString()
        Q5_df_fg = df.filter(df._c11 != "-").groupBy("_c11").count()
        Q5_answer = Q5_df_fg.orderBy(Q5_df_fg["count"].desc()).head(10)
        q5_answer = [Q5_answer[n].__getitem__("_c11") for n, i in enumerate(Q5_answer)]

        #6. If you select InterPRO features that are almost the same size (within 90-100%) as the protein itself, what is the top10 then?
        Q6_explain = df.withColumn("percentage", (df._c7 - df._c8) / df._c2).sort("percentage")
        Q6_df = df.withColumn("percentage", (df._c7 - df._c8) / df._c2).sort("percentage")
        Q6_answer = Q6_df.filter(df._c11 != "-").filter(Q6_df.percentage > 0.9).groupBy("_c11").count.sort("count, ascending = False").head(10)
        Q6_answer = [Q6_answer[n].__getitem__("_c11") for n, i in enumerate(Q6_answer)]

        #7. If you look at those features which also have textual annotation, what is the top 10 most common word found in that annotation?
        Q7_explain = 
        Q7_answer = 

        #8. And the top 10 least common?
        Q8_explain = 
        Q8_answer = 

        #9. Combining your answers for Q6 and Q7, what are the 10 most commons words found for the largest InterPRO features?
        Q9_explain = 
        Q9_answer = 

        #10. What is the coefficient of correlation ($R^2$) between the size of the protein and the number of features found?
        Q10_explain = 
        Q10_answer = 

        Question = list(range(1, 11))
        Answer = list([Q1_answer, Q2_answer, Q3_answer, Q4_answer, Q5_answer, Q6_answer, Q7_answer, Q8_answer, Q9_answer, Q10_answer])
        Explain = list([Q1_explain, Q2_explain, Q3_explain, Q4_explain, Q5_explain, Q6_explain, Q7_explain, Q8_explain, Q9_explain, Q10_explain])
        data = pd.DataFrame(list(zip(Question, Answer, Explain)), columns = ["Question", "Answer", "Explain"])
        data.to_csv("output/assignment5.csv", index=False)

#output should be csv with 3 columns:
    #1 question number
    #2 answer
    #3 scheduler's physical plan as string using .explain()

if __name__ == "__main__":
    #initiate object
    InterPRO_PS_obj = InterPRO_PS()
    #initiate session
    pss = InterPRO_PS_obj.start_sparksession("local[16]")
    #load the data
    path = "/data/dataprocessing/interproscan/all_bacilli.tsv"
    df = InterPRO_PS_obj.file_loader(path, "\t", pss)
    InterPRO_PS_obj.get_questions(df)
    pss.sparkContext.stop()
