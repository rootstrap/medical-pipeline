import json
import sys
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, FloatType, IntegerType
import os
from datetime import date



INPUT_DIR = os.environ.get('INPUT_DIR', '/input/')
RESULT_DIR = os.environ.get('RESULT_DIR', '/results/')

today = date.today()
today = today.strftime("%d%m%Y")

# Create Spark session
spark = SparkSession.builder.getOrCreate()

#Row example:
#Row(_code=417696007, _codingScheme='SNOMEDCT_US', _cui='C3536832', _disambiguated=False, _preferredText='Air', _score=0.0, _tui='T197', _xmi:id=116131)

def get_cui(row):
    return row['_cui']

# read xml files
rdd = spark.read.format('com.databricks.spark.xml').option("rowTag", "refsem:UmlsConcept").load(INPUT_DIR + today + '/*.xmi').rdd
rdd = rdd.flatMap(get_cui).map(lambda cui: (cui, 1)).reduceByKey(lambda a, b: a + b)

rdd.saveAsTextFile(RESULT_DIR + today)