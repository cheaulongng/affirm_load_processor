import logging
from collections import OrderedDict
import json

# ========================
# Conversion
# ========================
def to_int(val):
    return int(val) if val else None


def to_float(val):
    return float(val) if val else None


def get_key(bank_id, facility_id):
    return '{0}_{1}'.format(bank_id, facility_id if facility_id else '')


# ========================
# Misc
# ========================
def get_file_name(filename, path):
    return '{0}/{1}'.format(path, filename) if path else filename

# ========================
# Logging
# ========================
def get_logger(name):
    logger = logging.getLogger(name)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    return logger

# ========================
# Exception Handling
# ========================

def get_error_response_data(exception):
    error = OrderedDict()
    message = OrderedDict()
    message['value'] = get_exception_message(exception)
    error['message'] = message

    json_info = OrderedDict()
    json_info['error'] = error
    response = json.dumps(json_info)
    data = json.loads(response, object_pairs_hook=OrderedDict)

    return data


def get_exception_message(exception):
    try:
        type_name = type(exception)
        if type_name == str:
            err_msg = exception
        elif len(exception.args) > 0:
            err_msg = exception.args[0]
        else:
            err_msg = exception.description
    except:
        err_msg = 'Unhandled error'

    return err_msg


# ========================
# JSON handling
# ========================

def json_data(ordered_dict_data):
    jdata = json.dumps(ordered_dict_data)
    return json.loads(jdata, object_pairs_hook=OrderedDict)


def jsonify_standard_response(ordered_dict_data):
    json_data = OrderedDict()
    json_data['data'] = ordered_dict_data
    response = json.dumps(json_data)
    return json.loads(response, object_pairs_hook=OrderedDict)