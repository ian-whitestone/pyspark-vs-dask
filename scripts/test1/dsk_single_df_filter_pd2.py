import dask.bag

import logger

TEST_NAME = 'dsk_single_df_filter_pd2'
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

LOGGER.info('START: Starting to pandas..')
df = df.compute()
LOGGER.info('FINISH: hello pandas! %s', df.shape)
