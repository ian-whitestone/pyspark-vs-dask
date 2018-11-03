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

CREDIT_LIMITS = [0, 100, 500, 1000, 1500, 2000, 3000, 5000, 10000, 15000, 20000]
COUNTRIES = ['CAN', 'USA']
BUCKET = 'dask-avro-data'
SESSION = boto3.Session()
CLIENT = SESSION.client('s3')

SCHEMA = {
    'name': 'application',
    'type': 'record',
    'fields': [
        {
            'name': 'payload', 
            'type': {
                'type': 'record',
                'name': 'payload',
                'fields': [
                    {'name': 'applicationId', 'type': 'string'},
                    {'name': 'originationCountryCode', 'type': 'string'},
                    {'name': 'creationTimestamp', 'type': 'string'},
                    {
                        'name': 'applicant', 
                        'type': {
                            'name': 'applicant',
                            'type': 'record',
                            'fields': [
                                {'name': 'name', 'type': 'string'},
                                {'name': 'addressLine1', 'type': 'string'},
                                {'name': 'zip', 'type': 'string'},
                                {'name': 'city', 'type': 'string'},
                                {'name': 'state', 'type': 'string'},
                                {'name': 'country', 'type': 'string'}
                            ]
                        }
                    },
                    {
                        'name': 'phoneNumbers', 
                        'type': {
                            'name': 'phoneNumber',
                            'type': 'array',
                            'items': {
                                'name': 'Child',
                                'type': 'record',
                                'fields': [
                                    {'name': 'type', 'type': 'string'},
                                    {'name': 'value', 'type': 'string'}
                                ]
                            }
                        }
                    },
                    {'name': 'approved', 'type': 'boolean'},
                    {'name': 'creditLimit', 'type': 'int'},
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
                    {'name': 'ruleId', 'type': 'int'},
                    {'name': 'rulePass', 'type': 'boolean'},
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
                'applicant': {
                    'name': 'Some Name',
                    'addressLine1': 'Somewhere',
                    'zip': '12345',
                    'city': 'Nowhereville',
                    'state': 'NY',
                    'country': country
                },
                'originationCountryCode': random.choice(COUNTRIES, p=[0.02, 0.98]),
                'phoneNumbers': [
                    {'type': 'home', 'value': '111-123-4321'},
                    {'type': 'mobile', 'value': '999-123-1234'},
                ],
                'creationTimestamp': creationTimestamp,
                'approved': bool(random.randint(0, 1)),
                'creditLimit': random.choice(CREDIT_LIMITS)
            },
            'metadata': {
                'eventTimestamp': eventTimestamp,
                'ruleId': 123,
                'rulePass': True
            }
        }
        records.append(record)
    return records

def write_avro_records(id, records):
    fpath = 'app-{}.avro'.format(id)
    with open(fpath, 'wb') as out:
        writer(out, PARSED_SCHEMA, records)
    return fpath

LOGGER.info('Generating delayeds')
delayeds = []
for x in range(0, 200000):
    records = delayed(generate_records)(x)
    fpath = delayed(write_avro_records)(x, records)
    fpath = delayed(upload_to_s3)(BUCKET, fpath, 'application-data')
    res = delayed(os.remove)(fpath)
    delayeds.append(res)

LOGGER.info('Computing delayeds')
compute(delayeds, scheduler='threads', num_workers=10)