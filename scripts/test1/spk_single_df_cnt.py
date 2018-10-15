from pyspark import SparkConf, SparkContext, SQLContext

import logger

TEST_NAME = 'spk_single_df_cnt'
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH = "s3a://dask-avro-data/application-data/app-100*.avro"

# Start
LOGGER.info('START: Creating spark conf')
Sconf = SparkConf()
sc = SparkContext(appName="my_test", conf=Sconf)
sqlContext = SQLContext(sparkContext=sc)
LOGGER.info('FINISH: Finished creating spark conf')


LOGGER.info('START: Creating spark dataframe')
df = sqlContext.read.format("com.databricks.spark.avro").load(URLPATH)
LOGGER.info('FINISH: Spark dataframe created')

LOGGER.info('START: Starting count')
cnt = df.count()
LOGGER.info('FINISH: Count is %s', cnt)

sc.stop()