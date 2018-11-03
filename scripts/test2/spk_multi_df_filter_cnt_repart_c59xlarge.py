import os
import sys

from pyspark import SparkConf, SparkContext, SQLContext

import logger

MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
TEST_NAME = os.path.splitext(MODULE_NAME)[0]
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH1 = "s3a://dask-avro-data/application-data/app-*.avro"
URLPATH2 = "s3a://dask-avro-data/fulfillment-data/fulfillment-*.avro"

# Start
LOGGER.info('START: Creating spark conf')
Sconf = SparkConf().setMaster('local[12]'). \
    set('spark.driver.memory', '4g'). \
    set('spark.executor.memory', '5g')

sc = SparkContext(appName="my_test", conf=Sconf)
sqlContext = SQLContext(sparkContext=sc)
LOGGER.info('FINISH: Finished creating spark conf')

LOGGER.info('START: Creating spark dataframe 1')
df1 = sqlContext.read.format("com.databricks.spark.avro").load(URLPATH1)
df1 = df1.filter(df1.payload.originationCountryCode == 'CAN')
df1 = df1.selectExpr(
    "payload.applicationId as applicationId",
    "payload.creationTimestamp as creationTimestamp",
    "payload.approved as approved",
    "payload.creditLimit as creditLimit"
    )
LOGGER.info('FINISH: Spark dataframe 1 created')

LOGGER.info('START: Repartitioning df1')
df1 = df1.repartition(10)
LOGGER.info('FINISH: Repartitioning df1')

LOGGER.info('START: Creating spark dataframe 2')
df2 = sqlContext.read.format("com.databricks.spark.avro").load(URLPATH2)
df2 = df2.selectExpr(
    "payload.applicationId as applicationId",
    "payload.accountId as accountId",
    "payload.success as success"
    )
LOGGER.info('FINISH: Spark dataframe 2 created')

LOGGER.info('START: Repartitioning df2')
df2 = df2.repartition(10)
LOGGER.info('FINISH: Repartitioning df2')

LOGGER.info('START: Joining dataframes')
df = df1.join(df2, "applicationId", how='inner')
LOGGER.info('FINISH: Finished joining dataframes')

LOGGER.info('START: Starting filtered count')
cnt = df.count()
LOGGER.info('START: Count is %s', cnt)

sc.stop()