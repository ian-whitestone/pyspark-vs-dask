#!/bin/bash

# Parameters


# 1: aws_access_key_id
# 2: aws_secret_access_key

## Install through apt
echo "Install base applications..."
sudo apt-get update
sudo apt install -y vim git bzip2 -y
sudo apt install gcc g++ -y
sudo apt install python-dev -y

## Install aws cli
sudo apt install awscli -y

## Docker
sudo apt install docker.io -y
sudo usermod -a -G docker $USER # Allow user to run docker commands

# Install Miniconda
echo "Installing Miniconda"
cd ~
curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b

## Add a bunch of variables to the .bashrc file
echo 'Updating bashrc environment variables...'
echo 'export PATH="/home/ubuntu/miniconda3/bin:$PATH"' >> ~/.bashrc
echo ". /home/ubuntu/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
echo 'export EDITOR=vim' >> ~/.bashrc


chmod 700 ~/.bashrc

# Update environment variables with conda path before running commands below
export PATH="/home/ubuntu/miniconda3/bin:$PATH"
. /home/ubuntu/miniconda3/etc/profile.d/conda.sh # allows you to do conda activate isntead of source activate


## Dask Environment
conda create -n dask python=3.6 -y -q
conda activate dask
conda install dask -y
conda install s3fs -c conda-forge -y # dependency for reading S3 files
conda install fastavro -y
conda deactivate

# Spark Environment

## Install Java
sudo apt-get update
sudo apt-get install default-jre -y

## Spark Conda Env
conda create -n spark python=3.6 -y -q
conda activate spark
conda install -y conda=4.3.30
conda install -y pypandoc=1.4 py4j=0.10.7
conda install -y pandas # in order to convert spark dataframes back to pandas

## Download Stuff
wget http://repo1.maven.org/maven2/com/databricks/spark-avro_2.11/4.0.0/spark-avro_2.11-4.0.0.jar .
wget https://www.apache.org/dist/spark/spark-2.3.1/spark-2.3.1-bin-without-hadoop.tgz
wget https://archive.apache.org/dist/hadoop/core/hadoop-2.9.1/hadoop-2.9.1.tar.gz
tar -xvzf hadoop-2.9.1.tar.gz && rm -f hadoop-2.9.1.tar.gz
tar -xvzf spark-2.3.1-bin-without-hadoop.tgz && rm -f spark-2.3.1-bin-without-hadoop.tgz

## Install pyspark
cd spark-2.3.1-bin-without-hadoop/python
python setup.py install
conda deactivate

## Update bashrc
echo "#### SPARK CONFIGURATIONS ####" >> ~/.bashrc
echo "## JAVA_HOME" >> ~/.bashrc
echo 'export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")' >> ~/.bashrc
echo "## add hadoop to path" >> ~/.bashrc
echo 'export PATH=//home/ubuntu/hadoop-2.9.1/bin:$PATH' >> ~/.bashrc
echo "## add spark_to_path" >> ~/.bashrc
echo 'export PATH=//home/ubuntu/spark-2.3.1-bin-without-hadoop/sbin://home/ubuntu/spark-2.3.1-bin-without-hadoop/bin:$PATH' >> ~/.bashrc
echo "## spark distribution classpath" >> ~/.bashrc
echo 'export SPARK_DIST_CLASSPATH=$(hadoop classpath)://home/ubuntu/hadoop-2.9.1/share/hadoop/tools/lib/*://home/ubuntu/spark-avro_2.11-4.0.0.jar' >> ~/.bashrc
echo "## python fixing for conda environments" >> ~/.bashrc
echo 'export PYTHONPATH=//home/ubuntu/spark-2.3.1-bin-without-hadoop/python/lib/py4j-0.10.7-src.zip:/opt/spark-2.3.1-bin-without-hadoop/python' >> ~/.bashrc
echo "#### END SPARK CONFIGURATIONS ####" >> ~/.bashrc