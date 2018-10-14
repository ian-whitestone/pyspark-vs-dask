# Setup

## Single EC2 Instance

### Terraform Setup

Follow instructions [here](https://www.terraform.io/intro/getting-started/build.html).

```bash
terraform init
terraform plan
terraform apply
```
### Installing Dask


### Installing PySpark

## Download required files

```bash
wget https://www.apache.org/dist/spark/spark-2.3.1/spark-2.3.1-bin-without-hadoop.tgz

wget https://archive.apache.org/dist/hadoop/core/hadoop-2.9.1/hadoop-2.9.1.tar.gz
```

Download links reference:

- Spark: https://www.apache.org/dist/spark/spark-2.3.1/
- Hadoop: https://archive.apache.org/dist/hadoop/core/hadoop-2.9.1/

## Install Java

```bash
sudo apt-get update
sudo apt-get install default-jre -y
```

And verify installation:

```bash
>>> java -version
openjdk version "1.8.0_181"
OpenJDK Runtime Environment (build 1.8.0_181-8u181-b13-0ubuntu0.16.04.1-b13)
OpenJDK 64-Bit Server VM (build 25.181-b13, mixed mode)
```

## Unzip things

```bash
tar -xvzf hadoop-2.9.1.tar.gz && rm -f hadoop-2.9.1.tar.gz
tar -xvzf spark-2.3.1-bin-without-hadoop.tgz && rm -f spark-2.3.1-bin-without-hadoop.tgz
```

## Build conda environment

```bash
conda create -n spark python=3.6 -y -q
conda activate spark
conda install -y conda=4.3.30
conda install -y pypandoc=1.4 py4j=0.10.7
```

## Install pyspark

```bash
cd spark-2.3.1-bin-without-hadoop/python
python setup.py install
```

## Grab the spark-avro jar


```bash
cd /home/ubuntu
wget http://repo1.maven.org/maven2/com/databricks/spark-avro_2.11/4.0.0/spark-avro_2.11-4.0.0.jar .
```

## Update .bashrc


```bash
## JAVA_HOME
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
## add hadoop to path
export PATH=//home/ubuntu/hadoop-2.9.1/bin:$PATH
## add spark_to_path
export PATH=//home/ubuntu/spark-2.3.1-bin-without-hadoop/sbin://home/ubuntu/spark-2.3.1-bin-without-hadoop/bin:$PATH
## spark distribution classpath
export SPARK_DIST_CLASSPATH=$(hadoop classpath)://home/ubuntu/hadoop-2.9.1/share/hadoop/tools/lib/*://home/ubuntu/spark-avro_2.11-4.0.0.jar
## python fixing for conda environments
export PYTHONPATH=//home/ubuntu/spark-2.3.1-bin-without-hadoop/python/lib/py4j-0.10.7-src.zip:/opt/spark-2.3.1-bin-without-hadoop/python
```

## Verifying things are working

### Pure Python

```python
from pyspark import SparkConf, SparkContext, SQLContext
import datetime
import os

Sconf = SparkConf()
sc = SparkContext(appName="my_test", conf=Sconf)
## textfile = sc.textFile("s3a://<internal>/stuff.csv")
## sc.stop()

sqlContext = SQLContext(sparkContext=sc)

pa = '/home/ubuntu/data/0.avro'
df = sqlContext.read.format("com.databricks.spark.avro").load(pa)
print (df.count())
sc.stop()
```


### Pyspark

```bash
(spark) ubuntu@ip-172-31-2-44:~$ pyspark
Python 3.7.0 (default, Jun 28 2018, 13:15:42)
[GCC 7.2.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
2018-10-14 03:45:21 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.3.1
      /_/

Using Python version 3.7.0 (default, Jun 28 2018 13:15:42)
SparkSession available as 'spark'.

>>> pa = '/home/ubuntu/data/0.avro'
>>> df = spark.read.format("com.databricks.spark.avro").load(pa)
>>> df.count()
200

>>> pa = 's3a://dask-avro-data/0.avro'
>>> df = spark.read.format("com.databricks.spark.avro").load(pa)
```

### Datadog


*Resources*
- https://www.datadoghq.com/blog/monitoring-ec2-instances-with-datadog/


## Cluster Setup

Coming soon...