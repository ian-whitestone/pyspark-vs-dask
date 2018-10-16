# Setting Up Jupyter Lab on an EC2

1) Install Jupyter Lab

`conda install -c conda-forge jupyterlab -y`

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
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
c.NotebookApp.password = 'XXX' # from step 3
c.NotebookApp.certfile = '/home/ubuntu/mycert.pem' # created in step 2
```

5) Launch jupyter lab

`$ jupyter lab`


6) IP Address

Need to remote the 10 from the IP address, i.e.

Replace: `https://ip-10-202-130-71.kdc.<internal>.com:8888/`
With: `https://ip-202-130-71.kdc.<internal>.com:8888/`

# Resources

- http://jupyter-notebook.readthedocs.io/en/stable/public_server.html
- https://github.com/jupyter/notebook/issues/507


# Issues

Conda environments aren't showing up in available kernels despite having done:

```
$ conda install nb_conda_kernels -y
$ conda install nb_conda
```