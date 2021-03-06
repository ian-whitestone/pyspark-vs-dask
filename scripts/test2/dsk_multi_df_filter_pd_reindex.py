import sys
import os

import dask.bag
import dask.dataframe as dd

import logger

MODULE_NAME = os.path.basename(sys.modules['__main__'].__file__)
TEST_NAME = os.path.splitext(MODULE_NAME)[0]
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH1 = "s3://dask-avro-data/application-data/app-100*.avro"
URLPATH2 = "s3://dask-avro-data/fulfillment-data/fulfillment-100*.avro"

def filter_func(data):
    return data['payload']['originationCountryCode'] == 'CAN'

def parse_dict1(data):
    parsed = {
        'applicationId': data['payload']['applicationId'],
        'creationTimestamp': data['payload']['creationTimestamp'],
        'approved': data['payload']['approved'],
        'creditLimit': data['payload']['creditLimit']
    }
    return parsed

def parse_dict2(data):
    parsed = {
        'applicationId': data['payload']['applicationId'],
        'accountId': data['payload']['accountId'],
        'success': data['payload']['success'],
    }
    return parsed


# Start
LOGGER.info('START: Creating dask bag 1')
bag1 = dask.bag.read_avro(
    URLPATH1,
    storage_options = {
        'config_kwargs': {'max_pool_connections': 100} #To avoid connection pool is full errors, as discussed here: https://github.com/dask/dask/issues/3493
    },
    blocksize=None
)
bag1 = bag1.filter(filter_func)
bag1 = bag1.map(parse_dict1)
LOGGER.info('FINISH: Dask bag1 created')

LOGGER.info('START: Creating dask dataframe 1')
meta1 = {
    'applicationId': 'object',
    'creationTimestamp': 'object',
    'approved': 'bool',
    'creditLimit': 'int'
}
df1 = bag1.to_dataframe(meta=meta1)
LOGGER.info('FINISH: Dask dataframe 1 created')

LOGGER.info('START: Setting index on df1')
df1 = df1.set_index('applicationId')
LOGGER.info('START: Setting index on df1')

LOGGER.info('START: Creating dask bag 2')
bag2 = dask.bag.read_avro(
    URLPATH2,
    storage_options = {
        'config_kwargs': {'max_pool_connections': 100} #To avoid connection pool is full errors, as discussed here: https://github.com/dask/dask/issues/3493
    },
    blocksize=None
)
bag2 = bag2.map(parse_dict2)
LOGGER.info('FINISH: Dask bag2 created')

LOGGER.info('START: Creating dask dataframe 2')
meta2 = {
    'applicationId': 'object',
    'accountId': 'object',
    'success': 'bool',
}
df2 = bag2.to_dataframe(meta=meta2)
LOGGER.info('FINISH: Dask dataframe 2 created')

LOGGER.info('START: Setting index on df2')
df2 = df2.set_index('applicationId')
LOGGER.info('START: Setting index on df2')

LOGGER.info('START: Joining dataframes')
df = dd.merge(df1, df2, how='inner', left_on='applicationId', right_on='applicationId')
LOGGER.info('FINISH: Finished joining dataframes')

LOGGER.info('START: Starting to pandas..')
df = df.compute()
LOGGER.info('FINISH: hello pandas! %s', df.shape)
