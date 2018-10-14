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