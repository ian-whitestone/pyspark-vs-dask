
# Test Set 1 - Single Dataframe: read, filter and count/convert to pandas

All python scripts and logs are located in the `test1` directory. The python file/log corresponding to each test are named the same. For example, for test `dsk_single_df_single_file_cnt`, see the following files:

- Dask python script: `dsk_single_df_single_file_cnt.py`
- Dask log file: `logs/dsk_single_df_single_file_cnt.txt`
- Spark python script: `spk_single_df_single_file_cnt.py`
- Spark log file: `logs/spk_single_df_single_file_cnt.txt`

The `parselog.py` module is run to parse the log files and print the timings you see below. Example usage:

`$ python parselog.py test1/logs/dsk_single_df_single_file_cnt.txt`


## No Filter

### Single file

`URLPATH = "s3://dask-avro-data/application-data/app-100096.avro"`
- 998 records

**Dask**
```bash
0 (s) 0.00 (min): Creating dask bag
0 (s) 0.01 (min): Creating dask dataframe
0 (s) 0.00 (min): Starting count
0 (s) 0.01 (min): Total time for test: dsk_single_df_single_file_cnt
```

**PySpark**
```bash
2 (s) 0.03 (min): Creating spark conf
3 (s) 0.05 (min): Creating spark dataframe
1 (s) 0.02 (min): Starting count
6 (s) 0.11 (min): Total time for test: spk_single_df_single_file_cnt
```

### Multiple files
`URLPATH = "s3://dask-avro-data/application-data/app-100*.avro"`

- 842000 records

**Dask**
```bash
64 (s) 1.08 (min): Creating dask bag
21 (s) 0.36 (min): Creating dask dataframe
24 (s) 0.40 (min): Starting count
110 (s) 1.84 (min): Total time for test: dsk_single_df_cnt
```

**PySpark**
```bash
1 (s) 0.03 (min): Creating spark conf
85 (s) 1.43 (min): Creating spark dataframe
53 (s) 0.89 (min): Starting count
141 (s) 2.35 (min): Total time for test: spk_single_df_cnt
```


## With Filter

`URLPATH = "s3://dask-avro-data/application-data/app-100*.avro"`

- 842000 records

**Dask**
```bash
65 (s) 1.08 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
22 (s) 0.37 (min): Starting count
87 (s) 1.46 (min): Total time for test: dsk_single_df_filter_cnt
```

**PySpark**
```bash
1 (s) 0.03 (min): Creating spark conf
80 (s) 1.34 (min): Creating spark dataframe
71 (s) 1.19 (min): Starting filtered count
154 (s) 2.57 (min): Total time for test: spk_single_df_filter_cnt
```


`URLPATH = "s3://dask-avro-data/application-data/app-*.avro"`

- ~150,000,000 records... 3,000,000 after filtering


**Dask**
```bash
6686 (s) 111.43 (min): Creating dask bag with filter
26 (s) 0.43 (min): Creating dask dataframe
7468 (s) 124.47 (min): Starting count
14180 (s) 236.34 (min): Total time for test: dsk_single_df_filter_cnt2
```

**PySpark**
```bash
2 (s) 0.04 (min): Creating spark conf
1704 (s) 28.40 (min): Creating spark dataframe
15434 (s) 257.24 (min): Starting filtered count
17140 (s) 285.68 (min): Total time for test: spk_single_df_filter_cnt2
```

`URLPATH = "s3://dask-avro-data/application-data/app-*.avro"`

- ~150,000,000 records... 3,000,000 after filtering
- Dask: 
`cnt.compute(num_workers=100)` # number of threads
- Spark: 
`Sconf = SparkConf().setMaster('local[4]').set('spark.driver.memory', '20g')` # can only set number of cores, using max available


**Dask**
```bash
6586 (s) 109.78 (min): Creating dask bag with filter
27 (s) 0.45 (min): Creating dask dataframe
5276 (s) 87.95 (min): Starting count
11890 (s) 198.18 (min): Total time for test: dsk_single_df_filter_cnt3
```

**PySpark**
```bash
2 (s) 0.04 (min): Creating spark conf
1816 (s) 30.27 (min): Creating spark dataframe
16687 (s) 278.12 (min): Starting filtered count
18505 (s) 308.43 (min): Total time for test: spk_single_df_filter_cnt3
```
Not sure why timing went up...



`URLPATH = "s3://dask-avro-data/application-data/app-*.avro"`

- ~150,000,000 records... 3,000,000 after filtering
- Dask: 
`cnt.compute(num_workers=500)` # number of threads
- Spark: 
`Sconf = SparkConf().setMaster('local[4]')`


**Dask**
```bash
6645 (s) 110.75 (min): Creating dask bag with filter
26 (s) 0.45 (min): Creating dask dataframe
5397 (s) 89.95 (min): Starting count
12069 (s) 201.15 (min): Total time for test: dsk_single_df_filter_cnt4
```

**PySpark**
```bash
2 (s) 0.03 (min): Creating spark conf
1551 (s) 25.85 (min): Creating spark dataframe
14841 (s) 247.36 (min): Starting filtered count
16394 (s) 273.24 (min): Total time for test: spk_single_df_filter_cnt4
```

## With Filter to Pandas

`URLPATH = "s3://dask-avro-data/application-data/app-100*.avro"`

- 842000 records

**Dask**
```bash
70 (s) 1.18 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
25 (s) 0.43 (min): Starting to pandas..
96 (s) 1.61 (min): Total time for test: dsk_single_df_filter_pd
```

**PySpark**
```bash
2 (s) 0.03 (min): Creating spark conf
78 (s) 1.32 (min): Creating spark dataframe
73 (s) 1.23 (min): Starting to pandas..
154 (s) 2.58 (min): Total time for test: spk_single_df_filter_pd
```

# Test Set 2 - Multiple Dataframes: read, filter, join

## Join two dataframes, filter, convert to pandas

- 900,000 records/1200 avro files * 2 datasets

**DASK**
```bash
52 (s) 0.87 (min): Creating dask bag 1
0 (s) 0.00 (min): Creating dask dataframe 1
54 (s) 0.91 (min): Creating dask bag 2
0 (s) 0.00 (min): Creating dask dataframe 2
0 (s) 0.00 (min): Joining dataframes
665 (s) 11.09 (min): Starting to pandas..
772 (s) 12.87 (min): Total time for test: dsk_multi_df_filter_pd
```

**PYSPARK**

```bash
2 (s) 0.03 (min): Creating spark conf
93 (s) 1.56 (min): Creating spark dataframe 1
92 (s) 1.55 (min): Creating spark dataframe 2
0 (s) 0.00 (min): Joining dataframes
146 (s) 2.44 (min): Starting to pandas..
334 (s) 5.58 (min): Total time for test: spk_multi_df_filter_pd
```


### Join two dataframes, filter, and count


#### On a r5.xlarge (4 cores, 32GB Ram)
- 150,000,000 records/200,000 avro files * 2 datasets
- Note, ran out of disk space for dask. bumped up to 50GB EBS volume

**DASK**
```bash

```


**SPARK**

```bash
2 (s) 0.03 (min): Creating spark conf
1735 (s) 28.92 (min): Creating spark dataframe 1
1778 (s) 29.64 (min): Creating spark dataframe 2
0 (s) 0.00 (min): Joining dataframes
24383 (s) 406.40 (min): Starting filtered count
27900 (s) 465.00 (min): Total time for test: spk_multi_df_filter_cnt
```

#### On a c5.9xlarge (36 cores, 72 GB RAM)

**DASK**
```bash

```


- 12 spark cores
- 5 GB memory per worker
- 4 GB memory for master

**SPARK**
```bash
1 (s) 0.03 (min): Creating spark conf
627 (s) 10.46 (min): Creating spark dataframe 1
628 (s) 10.47 (min): Creating spark dataframe 2
0 (s) 0.00 (min): Joining dataframes
7695 (s) 128.26 (min): Starting filtered count
8953 (s) 149.22 (min): Total time for test: spk_multi_df_filter_cnt
```


#### With dask scheduler='processes' on the c5.9xlarge

**DASK**
```bash

```


# Test Set 3 - Running some Python UDFs

**Dask**
```bash

```

**PySpark**
```bash

```

# Test Set 4 - Scaling on a Single Machine

`dsk_filter_cnt` test with varying scheduler/num_workers

**Dask**
```bash
67 (s) 1.12 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
451 (s) 7.53 (min): Starting count
520 (s) 8.67 (min): Total time for test: dsk_filter_cnt_threading_36
81 (s) 1.36 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
454 (s) 7.57 (min): Starting count
536 (s) 8.94 (min): Total time for test: dsk_filter_cnt_threading_25
75 (s) 1.26 (min): Creating dask bag with filter
0 (s) 0.02 (min): Creating dask dataframe
448 (s) 7.48 (min): Starting count
524 (s) 8.75 (min): Total time for test: dsk_filter_cnt_threading_15
87 (s) 1.45 (min): Creating dask bag with filter
1 (s) 0.02 (min): Creating dask dataframe
417 (s) 6.96 (min): Starting count
506 (s) 8.43 (min): Total time for test: dsk_filter_cnt_threading_5
```

**PySpark**
```bash

```
