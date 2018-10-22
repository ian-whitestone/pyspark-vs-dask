import os
import sys

from pyspark import SparkConf, SparkContext, SQLContext

import logger

MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
TEST_NAME = os.path.splitext(MODULE_NAME)[0]
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH = "s3a://dask-avro-data/application-data/app-*.avro"

# Start
LOGGER.info('START: Creating spark conf')
Sconf = SparkConf().setMaster('local[4]').set('spark.driver.memory', '20g')
sc = SparkContext(appName="my_test", conf=Sconf)
sqlContext = SQLContext(sparkContext=sc)
LOGGER.info('FINISH: Finished creating spark conf')

LOGGER.info('START: Creating spark dataframe')
df = sqlContext.read.format("com.databricks.spark.avro").load(URLPATH)
LOGGER.info('FINISH: Spark dataframe created')


LOGGER.info('START: Starting filtered count')
cnt = df.filter(df.payload.originationCountryCode == 'CAN').count()
LOGGER.info('START: Count is %s', cnt)

sc.stop()