import csv
from models.models import Bank, Facility, Covenant
from common.utils import *

log = get_logger(__name__)

BANKS_DATA_FILENAME = 'banks.csv'
FACILITIES_DATA_FILENAME = 'facilities.csv'
COVENANTS_DATA_FILENAME = 'covenants.csv'


def load_banks(path=None):
    try:
        filename = get_file_name(BANKS_DATA_FILENAME, path)
        reader = csv.DictReader(open(filename, 'r'))
        banks = {}

        for line in reader:
            bank = Bank()
            bank.bank_id = to_int(line['id'])
            bank.bank_name = line['name']
            banks.update({str(bank.bank_id): bank})

        return banks

    except csv.Error as e:
        log.error('file {}, line {}: {}'.format(filename, reader.line_num, e))


def load_facilities(path=None):
    try:
        filename = get_file_name(FACILITIES_DATA_FILENAME, path)
        reader = csv.DictReader(open(filename, 'r'))
        facilities = {}

        for line in reader:
            bank_id = to_int(line['bank_id'])
            facility_id = to_int(line['id'])

            key = '{0}_{1}'.format(bank_id, facility_id)
            facility = Facility()
            facility.bank_id = bank_id
            facility.facility_id = facility_id
            facility.interest_rate = to_float(line['interest_rate'])
            facility.amount = to_int(float(line['amount']))

            facilities.update({key: facility})

        return facilities

    except csv.Error as e:
        log.error('file {}, line {}: {}'.format(filename, reader.line_num, e))


def load_covenants(path=None):
    try:
        filename = get_file_name(COVENANTS_DATA_FILENAME, path)
        reader = csv.DictReader(open(filename, 'r'))

        covenants = {}

        for line in reader:

            bank_id = to_int(line['bank_id'])
            facility_id = to_int(line['facility_id'])
            max_default_likelihood = to_float(line['max_default_likelihood'])
            banned_state = line['banned_state']

            key = '{0}_{1}'.format(bank_id, facility_id)
            covenant = covenants.get(key)

            if covenant:
                covenant.banned_states.append(banned_state)

                if max_default_likelihood:
                    covenant.max_default_likelihood = max_default_likelihood

            else:
                covenant = Covenant()
                covenant.bank_id = bank_id
                covenant.facility_id = facility_id
                covenant.max_default_likelihood = max_default_likelihood
                covenant.banned_states.append(banned_state)

                covenants.update({key: covenant})

        return covenants

    except csv.Error as e:
        log.error('file {}, line {}: {}'.format(filename, reader.line_num, e))

