import os
import logging

FORMAT = '%(asctime)s|%(levelname)s|%(name)s: %(message)s'

def get_logger(logname):
    filename = logname + '.txt'

    # delete file if it already exists
    if os.path.exists(filename):
        os.remove(filename)

    # set up logging to file
    logging.basicConfig(
         filename=filename,
         level=logging.INFO, 
         format=FORMAT,
     )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMAT)
    console.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger('logger')
    return logger