import sys
import os

import dask.bag
import dask.dataframe as dd

import logger

MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
TEST_NAME = os.path.splitext(MODULE_NAME)[0]
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH1 = "s3://dask-avro-data/application-data/app-10*.avro" # lg
URLPATH2 = "s3://dask-avro-data/application-data/app-100*.avro" # sm

def filter_func(data):
    return data['payload']['originationCountryCode'] == 'CAN'

for urlpath in [('lg', URLPATH1), ('sm', URLPATH2)]:
    scheduler = 'threading'
    for num_workers in [2, 4, 6, 20, 36]:
        size = urlpath[0]
        path = urlpath[1]

        test_name = "dsk_filter_pd_{}_{}_{}".format(size, scheduler, num_workers)
        LOGGER.info('BEGIN: Running test: {}'.format(test_name))

        LOGGER.info('START: Creating dask bag with filter')
        bag = dask.bag.read_avro(
            path,
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

        LOGGER.info('START: Starting to pandas')
        df = df.compute(scheduler=scheduler, num_workers=num_workers)
        LOGGER.info('FINISH: Hello pandas %s', df.shape)

        LOGGER.info('COMPLETE: Running test: {}'.format(test_name))

# Tried doing scheduler=processes, takes like over an hour....when num_workers=2
