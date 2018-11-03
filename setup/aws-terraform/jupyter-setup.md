# Setting Up Jupyter Lab on an EC2

1) Install Jupyter Lab

Run the following in your base (conda) environment.

```
conda install -c conda-forge jupyterlab -y
conda install jupyter -y
conda install nb_conda -y
```

2) Create certs

`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem`

Doesn't matter what your inputs are.

3) Create a hashed password

```python
In [1]: from notebook.auth import passwd
In [2]: passwd()
Enter password:
Verify password:
Out[2]: 'sha1:XXXXX'
```

4) Generate jupyter config

`$ jupyter notebook --generate-config`

`$ vi ~/.jupyter/jupyter_notebook_config.py`

Add this to bottom of config file:


```
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
c.NotebookApp.password = 'XXX' # from step 3
c.NotebookApp.certfile = '/home/ubuntu/mycert.pem' # created in step 2
```

5) Launch jupyter lab

`$ jupyter lab`


6) IP Address

Grab your `Public DNS (IPv4)` value from the EC2 dashboard in the AWS console.


`https://ec2-<public_ip_address>.compute-1.amazonaws.com:8888`


# Resources

- http://jupyter-notebook.readthedocs.io/en/stable/public_server.html
- https://github.com/jupyter/notebook/issues/507
- https://github.com/jupyter/notebook/issues/3946#issuecomment-423169943

# Get conda environment kernels showing up in jupyter lab

Run the following with your environment activated

```
$ conda install nb_conda_kernels -y
$ conda install nb_conda -y
```