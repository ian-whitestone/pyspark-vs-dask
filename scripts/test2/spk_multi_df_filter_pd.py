from pyspark import SparkConf, SparkContext, SQLContext

import logger

TEST_NAME = 'spk_multi_df_filter_pd'
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH1 = "s3a://dask-avro-data/application-data/app-100*.avro"
URLPATH2 = "s3a://dask-avro-data/fulfillment-data/fulfillment-100*.avro"

# Start
LOGGER.info('START: Creating spark conf')
Sconf = SparkConf()
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

LOGGER.info('START: Creating spark dataframe 2')
df2 = sqlContext.read.format("com.databricks.spark.avro").load(URLPATH2)
df2 = df2.selectExpr(
    "payload.applicationId as applicationId",
    "payload.accountId as accountId",
    "payload.success as success"
    )
LOGGER.info('FINISH: Spark dataframe 2 created')

LOGGER.info('START: Joining dataframes')
df = df1.join(df1, df1.applicationId == df2.applicationId, how='inner')
LOGGER.info('FINISH: Finished joining dataframes')

LOGGER.info('START: Starting to pandas..')
df = df.toPandas()
LOGGER.info('FINISH: hello pandas! %s', df.shape)

sc.stop()