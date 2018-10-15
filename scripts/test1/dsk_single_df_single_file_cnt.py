import dask.bag

import logger

TEST_NAME = 'dsk_single_df_single_file_cnt'
LOGGER = logger.get_logger(TEST_NAME)

# Specify some constants
URLPATH = "s3://dask-avro-data/application-data/app-100096.avro"

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
