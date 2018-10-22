import sys
import os
import dask.bag

import logger

MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
TEST_NAME = os.path.splitext(MODULE_NAME)[0]
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH = "s3://dask-avro-data/application-data/app-100*.avro"

# Start
LOGGER.info('START: Creating dask bag')
bag = dask.bag.read_avro(URLPATH)
LOGGER.info('FINISH: Dask bag created')

LOGGER.info('START: Creating dask dataframe')
df = bag.to_dataframe()
LOGGER.info('FINISH: Dask dataframe created')

LOGGER.info('START: Starting count')
cnt = len(df.payload)
LOGGER.info('FINISH: Count is %s', cnt)
