import logging

def read_input(fp):
    logging.info("Reading file: " + fp)
    with open(fp) as fh:
        f = fh.read()
    return f.split('\n')