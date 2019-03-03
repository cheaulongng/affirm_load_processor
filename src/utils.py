import logging


def get_file_name(filename, path):
    return '{0}/{1}'.format(path, filename) if path else filename


def to_int(val):
    return int(val) if val else None


def to_float(val):
    return float(val) if val else None


def get_key(bank_id, facility_id):
    return '{0}_{1}'.format(bank_id, facility_id if facility_id else '')


def get_logger(name):
    logger = logging.getLogger(name)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    return logger