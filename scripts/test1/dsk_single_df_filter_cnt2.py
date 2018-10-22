import sys
import os
import dask.bag

import logger

MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
TEST_NAME = os.path.splitext(MODULE_NAME)[0]
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH = "s3://dask-avro-data/application-data/app-*.avro"

def filter_func(data):
    return data['payload']['originationCountryCode'] == 'CAN'

# Start
LOGGER.info('START: Creating dask bag with filter')
bag = dask.bag.read_avro(URLPATH)
bag = bag.filter(filter_func)
LOGGER.info('FINISH: Dask bag created')

LOGGER.info('START: Creating dask dataframe')
df = bag.to_dataframe(meta={'payload': 'object', 'metadata': 'object'})
LOGGER.info('FINISH: Dask dataframe created')

LOGGER.info('START: Starting count')
cnt = len(df.payload)
LOGGER.info('FINISH: Count is %s', cnt)
