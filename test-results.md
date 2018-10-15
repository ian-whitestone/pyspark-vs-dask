
# Test Set 1 - Single Dataframe: read, filter and count/convert to pandas

All python scripts and logs are located in the `test1` directory. The python file/log corresponding to each test are named the same. For example, for test `dsk_single_df_single_file_cnt`, see the following files:

- Dask python script: `dsk_single_df_single_file_cnt.py`
- Dask log file: `dsk_single_df_single_file_cnt.txt`
- Spark python script: `spk_single_df_single_file_cnt.py`
- Spark log file: `spk_single_df_single_file_cnt.txt`

The `parselog.py` module is run to parse the log files and print the timings you see below. Example usage:

`$ python parselog.py test1/dsk_single_df_single_file_cnt.txt`



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

`URLPATH = "s3://dask-avro-data/application-data/app-*.avro"`

- records


**Dask**
```bash

```

**PySpark**
```bash

```
# Test Set 2 - Multiple Dataframes: read, filter, join


**Dask**
```bash

```

**PySpark**
```bash

```