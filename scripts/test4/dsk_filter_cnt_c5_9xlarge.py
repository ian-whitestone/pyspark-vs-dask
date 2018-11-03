import sys
import os

import dask.bag
import dask.dataframe as dd

from dask.multiprocessing import get as mp_get
from dask.threaded import get as th_get
from dask import get as s_get


import logger

MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
TEST_NAME = os.path.splitext(MODULE_NAME)[0]
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH1 = "s3://dask-avro-data/application-data/app-10*.avro"
URLPATH2 = "s3://dask-avro-data/fulfillment-data/fulfillment-10*.avro"


def filter_func(data):
    return data['payload']['originationCountryCode'] == 'USA'


for num_workers in [2, 3, 4, 6, 16, 26, 36]:
    test_name = "dsk_filter_cnt_{}_{}".format('threading', num_workers)
    LOGGER.info('BEGIN: Running test: {}'.format(test_name))

    LOGGER.info('START: Creating dask bag with filter')
    bag = dask.bag.read_avro(
        URLPATH1,
        storage_options={
            'config_kwargs': {'max_pool_connections': 500}
        },
        blocksize=None
    )
    bag = bag.filter(filter_func)
    LOGGER.info('FINISH: Dask bag created')

    LOGGER.info('START: Creating dask dataframe')
    df = bag.to_dataframe(meta={'payload': 'object', 'metadata': 'object'})
    LOGGER.info('FINISH: Dask dataframe created')

    LOGGER.info('START: Starting count')
    cnt = df.payload.count().compute(scheduler='threading', num_workers=num_workers)
    LOGGER.info('FINISH: Count is %s', cnt)

    LOGGER.info('COMPLETE: Running test: {}'.format(test_name))

