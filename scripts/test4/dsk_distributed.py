import sys
import os

import dask.bag
import dask.dataframe as dd
from dask.distributed import Client, LocalCluster

import logger


if __name__ == '__main__':
    MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
    TEST_NAME = os.path.splitext(MODULE_NAME)[0]
    LOGGER = logger.get_logger(TEST_NAME)
    # Specify some constants
    URLPATH1 = "s3://dask-avro-data/application-data/app-1000*.avro"

    def filter_func(data):
        return data['payload']['originationCountryCode'] == 'CAN'


    for conf in [(1, 36), (4, 9), (12, 3), (36, 1)]:
        n_workers = conf[0]
        threads_per_worker = conf[1]

        test_name = "dsk_filter_pd_dist_{}_{}".format(n_workers, threads_per_worker)
        LOGGER.info('BEGIN: Running test: {}'.format(test_name))

        cluster = LocalCluster(
            n_workers=n_workers, threads_per_worker=threads_per_worker)
        client = Client(cluster)

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

        LOGGER.info('START: Starting to pandas')
        df = df.compute()
        LOGGER.info('FINISH: Hello pandas %s', df.shape)

        client.close()
        LOGGER.info('COMPLETE: Running test: {}'.format(test_name))
