
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


## Join two dataframes, filter, and count


### On a r5.xlarge (4 cores, 32GB Ram)
- 150,000,000 records/200,000 avro files * 2 datasets
- Note, ran out of disk space for dask. bumped up to 50GB EBS volume

**DASK**
Didn't finish (ran for over a day).


**SPARK**

```bash
2 (s) 0.03 (min): Creating spark conf
1735 (s) 28.92 (min): Creating spark dataframe 1
1778 (s) 29.64 (min): Creating spark dataframe 2
0 (s) 0.00 (min): Joining dataframes
24383 (s) 406.40 (min): Starting filtered count
27900 (s) 465.00 (min): Total time for test: spk_multi_df_filter_cnt
```

### On a c5.9xlarge (36 cores, 72 GB RAM)

**DASK**
Didn't finish (ran for over a day).


**SPARK**

- 12 spark cores
- 5 GB memory per worker
- 4 GB memory for master

```bash
1 (s) 0.03 (min): Creating spark conf
627 (s) 10.46 (min): Creating spark dataframe 1
628 (s) 10.47 (min): Creating spark dataframe 2
0 (s) 0.00 (min): Joining dataframes
7695 (s) 128.26 (min): Starting filtered count
8953 (s) 149.22 (min): Total time for test: spk_multi_df_filter_cnt
```

## Join two dataframes, repartition, filter, and count
The dask docs discuss [repartitioning & reindexing](http://docs.dask.org/en/latest/dataframe-performance.html) as ways to improve performance with distributed dataframes.

### dsk_multi_df_filter_pd.py

#### r5.xlarge

You can see the speed up that re-indexing and repartitioning bring:

rerun of original:

`dsk_multi_df_filter_pd.py`

```bash
54 (s) 0.92 (min): Creating dask bag 1
0 (s) 0.00 (min): Creating dask dataframe 1
55 (s) 0.92 (min): Creating dask bag 2
0 (s) 0.00 (min): Creating dask dataframe 2
0 (s) 0.00 (min): Joining dataframes
721 (s) 12.03 (min): Starting to pandas..
832 (s) 13.87 (min): Total time for test: dsk_multi_df_filter_pd
```

with repartition:

`dsk_multi_df_filter_pd_repart.py`

```bash
55 (s) 0.92 (min): Creating dask bag 1
0 (s) 0.00 (min): Creating dask dataframe 1
0 (s) 0.00 (min): Repartitioning df1 with 10 parts
55 (s) 0.92 (min): Creating dask bag 2
0 (s) 0.00 (min): Creating dask dataframe 2
0 (s) 0.00 (min): Repartitioning df2 with 10 parts
0 (s) 0.00 (min): Joining dataframes
53 (s) 0.89 (min): Starting to pandas..
163 (s) 2.73 (min): Total time for test: dsk_multi_df_filter_pd_repart
```

with reindex:

`dsk_multi_df_filter_pd_reindex.py`

```bash
54 (s) 0.90 (min): Creating dask bag 1
0 (s) 0.00 (min): Creating dask dataframe 1
32 (s) 0.55 (min): Setting index on df1
56 (s) 0.94 (min): Creating dask bag 2
0 (s) 0.00 (min): Creating dask dataframe 2
20 (s) 0.33 (min): Setting index on df2
0 (s) 0.00 (min): Joining dataframes
62 (s) 1.04 (min): Starting to pandas..
226 (s) 3.77 (min): Total time for test: dsk_multi_df_filter_pd_reindex
```

### `dsk_multi_df_filter_cnt.py`

Recall, the original didn't finish...

##### r5.xlarge
**Note**: the partition splits below document the number of partitions used for df1 (which gets filtered), and df2, respectively.

with 10/100 partitions and 4 workers

```bash
64 (s) 1.08 (min): Creating dask bag 1
25 (s) 0.43 (min): Creating dask dataframe 1
0 (s) 0.00 (min): Repartitioning df1 with 10 parts
64 (s) 1.07 (min): Creating dask bag 2
20 (s) 0.35 (min): Creating dask dataframe 2
0 (s) 0.00 (min): Repartitioning df2 with 100 parts
1 (s) 0.03 (min): Joining dataframes
10905 (s) 181.75 (min): Starting count
11083 (s) 184.72 (min): Total time for test: dsk_multi_df_filter_cnt_repart
```

##### c5.9xlarge

with 10/10 partitions and 10 workers:

```bash
56 (s) 0.94 (min): Creating dask bag 1
23 (s) 0.40 (min): Creating dask dataframe 1
0 (s) 0.00 (min): Repartitioning df1 with 10 parts
60 (s) 1.00 (min): Creating dask bag 2
19 (s) 0.32 (min): Creating dask dataframe 2
0 (s) 0.00 (min): Repartitioning df2 with 10 parts
1 (s) 0.03 (min): Joining dataframes
7650 (s) 127.52 (min): Starting count
7812 (s) 130.21 (min): Total time for test: dsk_multi_df_filter_cnt_repart
```

with 20/20 partitions and 20 workers:

```bash
59 (s) 0.98 (min): Creating dask bag 1
23 (s) 0.39 (min): Creating dask dataframe 1
0 (s) 0.00 (min): Repartitioning df1 with 20 parts
62 (s) 1.04 (min): Creating dask bag 2
19 (s) 0.32 (min): Creating dask dataframe 2
0 (s) 0.00 (min): Repartitioning df2 with 20 parts
1 (s) 0.03 (min): Joining dataframes
7875 (s) 131.26 (min): Starting count
8042 (s) 134.04 (min): Total time for test: dsk_multi_df_filter_cnt_repart_c59xlarge
```



### `spk_multi_df_filter_cnt.py`

#### c5.9xlarge

with 12/12 partitions, and 12 cores (workers)

```python
Sconf = SparkConf().setMaster('local[12]'). \
    set('spark.driver.memory', '4g'). \
    set('spark.executor.memory', '5g')
```

```bash
2 (s) 0.04 (min): Creating spark conf
651 (s) 10.86 (min): Creating spark dataframe 1
0 (s) 0.00 (min): Repartitioning df1
679 (s) 11.32 (min): Creating spark dataframe 2
0 (s) 0.00 (min): Repartitioning df2
0 (s) 0.00 (min): Joining dataframes
8287 (s) 138.12 (min): Starting filtered count
9620 (s) 160.35 (min): Total time for test: spk_multi_df_filter_cnt_repart_c59xlarge
```


# Test Set 3 - Running some Python UDFs

**Dask**
```bash

```

**PySpark**
```bash

```

# Test Set 4 - Scaling on a Single Machine

`dsk_filter_cnt` test with varying num_workers

**Dask**
```bash
54 (s) 0.90 (min): Creating dask bag with filter
0 (s) 0.02 (min): Creating dask dataframe
539 (s) 9.00 (min): Starting count
594 (s) 9.92 (min): Total time for test: dsk_filter_cnt_threading_2
56 (s) 0.94 (min): Creating dask bag with filter
1 (s) 0.02 (min): Creating dask dataframe
361 (s) 6.02 (min): Starting count
418 (s) 6.98 (min): Total time for test: dsk_filter_cnt_threading_3
55 (s) 0.93 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
238 (s) 3.97 (min): Starting count
294 (s) 4.91 (min): Total time for test: dsk_filter_cnt_threading_4
```

**PySpark**
```bash

```

`dsk_filter_cnt_c5_9xlarge`

- run the same tests as above on a bigger EC2 instance with more cores..

**Dask**

```bash
54 (s) 0.90 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
518 (s) 8.63 (min): Starting count
572 (s) 9.55 (min): Total time for test: dsk_filter_cnt_threading_2
52 (s) 0.88 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
337 (s) 5.62 (min): Starting count
391 (s) 6.52 (min): Total time for test: dsk_filter_cnt_threading_3
54 (s) 0.92 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
226 (s) 3.77 (min): Starting count
281 (s) 4.70 (min): Total time for test: dsk_filter_cnt_threading_4
53 (s) 0.89 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
181 (s) 3.03 (min): Starting count
235 (s) 3.93 (min): Total time for test: dsk_filter_cnt_threading_6
53 (s) 0.89 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
172 (s) 2.88 (min): Starting count
227 (s) 3.79 (min): Total time for test: dsk_filter_cnt_threading_16
53 (s) 0.90 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
182 (s) 3.04 (min): Starting count
237 (s) 3.95 (min): Total time for test: dsk_filter_cnt_threading_26
55 (s) 0.92 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
183 (s) 3.07 (min): Starting count
239 (s) 4.00 (min): Total time for test: dsk_filter_cnt_threading_36
```

- you can see effect of adding more workers has diminishing returns



`dsk_filter_cnt_compute_get`

- compare threaded scheduler to synchronous scheduler

**Dask**

```bash
53 (s) 0.90 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
528 (s) 8.81 (min): Starting count
583 (s) 9.73 (min): Total time for test: dsk_filter_cnt_threaded_2
54 (s) 0.91 (min): Creating dask bag with filter
0 (s) 0.02 (min): Creating dask dataframe
384 (s) 6.40 (min): Starting count
439 (s) 7.33 (min): Total time for test: dsk_filter_cnt_threaded_3
57 (s) 0.96 (min): Creating dask bag with filter
1 (s) 0.02 (min): Creating dask dataframe
304 (s) 5.07 (min): Starting count
362 (s) 6.05 (min): Total time for test: dsk_filter_cnt_threaded_4
58 (s) 0.97 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
1051 (s) 17.52 (min): Starting count
1110 (s) 18.51 (min): Total time for test: dsk_filter_cnt_synchronous_1
```



`dsk_filter_pd`

- filter a dataset, and convert it to a pandas dataframe
- `sm` is a smaller dataset, `application-data/app-100*.avro`
- `lg` is a larger dataset, `application-data/app-10*.avro`

**Dask**

```bash
52 (s) 0.87 (min): Creating dask bag with filter
0 (s) 0.00 (min): Creating dask dataframe
52 (s) 0.87 (min): Starting to pandas
104 (s) 1.74 (min): Total time for test: dsk_filter_pd_sm_threading_2
54 (s) 0.91 (min): Creating dask bag with filter
0 (s) 0.00 (min): Creating dask dataframe
28 (s) 0.48 (min): Starting to pandas
83 (s) 1.39 (min): Total time for test: dsk_filter_pd_sm_threading_4
52 (s) 0.88 (min): Creating dask bag with filter
0 (s) 0.00 (min): Creating dask dataframe
19 (s) 0.33 (min): Starting to pandas
72 (s) 1.21 (min): Total time for test: dsk_filter_pd_sm_threading_6
49 (s) 0.83 (min): Creating dask bag with filter
0 (s) 0.00 (min): Creating dask dataframe
16 (s) 0.28 (min): Starting to pandas
66 (s) 1.11 (min): Total time for test: dsk_filter_pd_sm_threading_20
54 (s) 0.91 (min): Creating dask bag with filter
0 (s) 0.00 (min): Creating dask dataframe
16 (s) 0.28 (min): Starting to pandas
71 (s) 1.18 (min): Total time for test: dsk_filter_pd_sm_threading_36
54 (s) 0.91 (min): Creating dask bag with filter
0 (s) 0.01 (min): Creating dask dataframe
594 (s) 9.90 (min): Starting to pandas
649 (s) 10.83 (min): Total time for test: dsk_filter_pd_lg_threading_2
51 (s) 0.87 (min): Creating dask bag with filter
1 (s) 0.02 (min): Creating dask dataframe
282 (s) 4.70 (min): Starting to pandas
335 (s) 5.59 (min): Total time for test: dsk_filter_pd_lg_threading_4
52 (s) 0.87 (min): Creating dask bag with filter
1 (s) 0.02 (min): Creating dask dataframe
212 (s) 3.54 (min): Starting to pandas
265 (s) 4.43 (min): Total time for test: dsk_filter_pd_lg_threading_6
51 (s) 0.86 (min): Creating dask bag with filter
1 (s) 0.02 (min): Creating dask dataframe
177 (s) 2.96 (min): Starting to pandas
230 (s) 3.85 (min): Total time for test: dsk_filter_pd_lg_threading_20
64 (s) 1.07 (min): Creating dask bag with filter
1 (s) 0.02 (min): Creating dask dataframe
180 (s) 3.00 (min): Starting to pandas
245 (s) 4.10 (min): Total time for test: dsk_filter_pd_lg_threading_36
```

- appears to peak at 20 threads
