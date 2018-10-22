import sys
import os

import dask.bag
import dask.dataframe as dd

import logger

MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
TEST_NAME = os.path.splitext(MODULE_NAME)[0]
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH1 = "s3://dask-avro-data/application-data/app-10*.avro"
URLPATH2 = "s3://dask-avro-data/fulfillment-data/fulfillment-10*.avro"


def filter_func(data):
    return data['payload']['originationCountryCode'] == 'USA'

for scheduler in ['threading', 'processes']:
    for num_workers in [36, 25, 15, 5]:

        test_name = "dsk_filter_cnt_{}_{}".format(scheduler, num_workers)
        LOGGER.info('BEGIN: Running test: {}'.format(test_name))

        LOGGER.info('START: Creating dask bag with filter')
        bag = dask.bag.read_avro(
            URLPATH1,
            storage_options={
                'config_kwargs': {'max_pool_connections': 500}
            }, 
            blocksize=None)
        bag = bag.filter(filter_func)
        LOGGER.info('FINISH: Dask bag created')

        LOGGER.info('START: Creating dask dataframe')
        df = bag.to_dataframe(meta={'payload': 'object', 'metadata': 'object'})
        LOGGER.info('FINISH: Dask dataframe created')

        LOGGER.info('START: Starting count')
        cnt = df.payload.count().compute(
            scheduler=scheduler, num_workers=num_workers)
        LOGGER.info('FINISH: Count is %s', cnt)

        LOGGER.info('COMPLETE: Running test: {}'.format(test_name))


# On processes-36, dont see more than 1 python process running during compute step...