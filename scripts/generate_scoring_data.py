"""Generate a bunch of fake avro data (simulating credit card application data) 
and upload to s3.

Running in python 3.7. Installed the following:
- pip install fastavro
- pip install boto3
"""

import logging
import os
import time

from fastavro import writer, parse_schema
import boto3
from dask import delayed, compute
from numpy import random


LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

BUCKET = 'dask-avro-data'
SESSION = boto3.Session()
CLIENT = SESSION.client('s3')

SCHEMA = {
    'name': 'scoring',
    'type': 'record',
    'fields': [
        {
            'name': 'payload', 
            'type': {
                'type': 'record',
                'name': 'payload',
                'fields': [
                    {'name': 'applicationId', 'type': 'string'},
                    {'name': 'score', 'type': 'float'},
                    {'name': 'creationTimestamp', 'type': 'string'},
                    {'name': 'error', 'type': 'boolean'},
                ]
            }
        },
        {
            'name': 'metadata', 
            'type': {
                'type': 'record',
                'name': 'metadata',
                'fields': [
                    {'name': 'eventTimestamp', 'type': 'string'},
                ]
            }
        }
    ],
}

PARSED_SCHEMA = parse_schema(SCHEMA)


def upload_to_s3(bucket, fpath, prefix=''):
    """Upload a file to s3.
    
    Parameters
    ----------
    bucket : str
        Name of the S3 bucket
    fpath : str
        Path to the file
    prefix : str
        Prefix to add to filename to create key
    Returns
    --------
    str
        Return the filepath so the next function in the task graph
        will be reliant on upload_to_s3
    """
    fname = os.path.basename(fpath)
    key = os.path.join(prefix, fname)
    with open(fpath, 'rb') as f_in:
        CLIENT.put_object(Bucket=bucket, Key=key, Body=f_in)
    return fpath


def generate_records(id):
    epoch = random.randint(1347517370000, 1397517370000)/1000
    time_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    creationTimestamp = time.strftime(time_fmt, time.localtime(epoch))
    eventTimestamp = time.strftime(time_fmt, time.localtime(epoch))

    records = []
    for x in range(0, random.randint(500, 1000)):
        record = {
            'payload': {
                'applicationId': '{}-{}'.format(id, x),
                'score': random.random(),
                'creationTimestamp': creationTimestamp,
                'error': bool(random.choice([0, 1], p=[0.999, 0.001])),
            },
            'metadata': {
                'eventTimestamp': eventTimestamp
            }
        }
        records.append(record)
    return records

def write_avro_records(id, records):
    fpath = 'scoring-{}.avro'.format(id)
    with open(fpath, 'wb') as out:
        writer(out, PARSED_SCHEMA, records)
    return fpath 

LOGGER.info('Generating delayeds')
delayeds = []
for x in range(0, 200000):
    records = delayed(generate_records)(x)
    fpath = delayed(write_avro_records)(x, records)
    fpath = delayed(upload_to_s3)(BUCKET, fpath, 'scoring-data')
    res = delayed(os.remove)(fpath)
    delayeds.append(res)

LOGGER.info('Computing delayeds')
compute(delayeds, scheduler='threads', num_workers=20)