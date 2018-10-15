from pyspark import SparkConf, SparkContext, SQLContext

import logger

TEST_NAME = 'spk_single_df_filter_cnt'
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH = "s3a://dask-avro-data/application-data/app-100*.avro"

# Start
LOGGER.info('START: Creating spark conf')
Sconf = SparkConf()
sc = SparkContext(appName="my_test", conf=Sconf)
sqlContext = SQLContext(sparkContext=sc)
LOGGER.info('FINISH: Finished creating spark conf')

URLPATH = "s3a://dask-avro-data/application-data/app-100*.avro"

LOGGER.info('START: Creating spark dataframe')
df = sqlContext.read.format("com.databricks.spark.avro").load(URLPATH)
LOGGER.info('FINISH: Spark dataframe created')

LOGGER.info('START: Starting filtered count')
cnt = df.filter(df.payload.originationCountryCode == 'CAN').count()
LOGGER.info('START: Count is %s', cnt)

sc.stop()