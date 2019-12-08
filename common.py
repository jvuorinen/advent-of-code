import logging

def read_input(fp):
    logging.info("Reading file: " + fp)
    with open(fp) as fh:
        result = fh.read()
        
    return result.split('\n')