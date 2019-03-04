# process_loans.py
"""
This is an utility script to process loans from loan.csv.

Usage:
    python process_loans.py <filename>

If filename is not provided, default loan.csv file will be used)
Two output files (assignments.csv, yields.csv) will be generated to "output" folder

Example:
    python process_loans.py files/loans.csv
"""

import csv
import os
import sys
from services.loan_service import LoanService
from models.models import Loan
from services.finance_data import load_facilities, load_covenants
from common.utils import *


log = get_logger(__name__)


ASSIGNMENTS_FILENAME = 'assignments.csv'
YIELDS_FILENAME = 'yields.csv'
DEFAULT_LOAN_FILE = 'loans.csv'


def process_all_loans(filename):
    try:
        path = os.path.dirname(filename)

        # Preload finance data for loan processing
        facilities = load_facilities(path)
        covenants = load_covenants(path)

        # Process loans
        processor = LoanService(facilities, covenants)
        reader = csv.DictReader(open(filename, 'r'))
        loan_assignments = []

        log.info('START Processing Loans')

        for line in reader:
            loan = Loan()
            loan.loan_id = to_int(line['id'])
            loan.amount = to_int(line['amount'])
            loan.interest_rate = to_float(line['interest_rate'])
            loan.default_likelihood = to_float(line['default_likelihood'])
            loan.state = line['state']

            loan_assignment = processor.process_loan(loan)
            if loan_assignment:
                loan_assignments.append(loan_assignment)

                log.info('Process loan_id: {0}, funded facility_id: {1}, expected_yield: {2}'
                         .format(loan_assignment.loan_id,
                                 loan_assignment.facility_id,
                                 to_int(loan_assignment.expected_yield)))

        # Generate output files
        _generate_assignments_output_file(loan_assignments, 'output')
        _generate_facility_yields_output_file(processor.get_facility_yields(), 'output')

        log.info('END Processing Loans')

    except Exception as e:
        log.error(e)


def _generate_assignments_output_file(assignments, path):
    filename = get_file_name(ASSIGNMENTS_FILENAME, path)

    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['loan_id', 'facility_id'])

        for assignment in assignments:
            writer.writerow([assignment.loan_id, assignment.facility_id])

    log.info('Generate {}'.format(filename))


def _generate_facility_yields_output_file(facility_yields, path):
    filename = get_file_name(YIELDS_FILENAME, path)

    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['facility_id', 'expected_yield'])

        for key, facility_yield in facility_yields.items():
            writer.writerow([facility_yield.facility_id, to_int(facility_yield.expected_yield)])

    log.info('Generate {}'.format(filename))


if __name__ == '__main__':
    try:
        # Default file
        filename = get_file_name(DEFAULT_LOAN_FILE, 'data_files')

        # Get loan file from command argument
        args = sys.argv
        if len(args) > 1:
            filename = args[1]

        process_all_loans(filename)

    except Exception as e:
        log.error(e)