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
from loan_processor import LoanProcessor
from models import Loan
from finance_data import load_facilities, load_covenants
from utils import *


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
        processor = LoanProcessor(facilities, covenants)
        reader = csv.DictReader(open(filename, 'r'))
        loan_assignments = []

        log.info('START Processing Loans')

        for line in reader:
            loan = Loan()
            loan.id = to_int(line['id'])
            loan.amount = to_int(line['amount'])
            loan.interest_rate = to_float(line['interest_rate'])
            loan.default_likelihood = to_float(line['default_likelihood'])
            loan.state = line['state']

            loan_assignment = processor.process_loan(loan)
            loan_assignments.append(loan_assignment)

            log.info('Process loan_id: {0}, funded facility_id: {1}'.format(loan_assignment.loan_id, loan_assignment.facility_id))

        # Generate output files
        log.info('Generate assignments.csv')
        _generate_assignments_output_file(loan_assignments, 'output')

        log.info('Generate yields.csv')
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


def _generate_facility_yields_output_file(facility_yields, path):
    filename = get_file_name(YIELDS_FILENAME, path)

    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['facility_id', 'expected_yield'])

        for facility_yield in facility_yields:
            writer.writerow([facility_yield.facility_id, facility_yield.expected_yield])


if __name__ == '__main__':
    try:
        # Default file
        filename = get_file_name(DEFAULT_LOAN_FILE, 'files')

        # Get loan file from command argument
        args = sys.argv
        if len(args) > 1:
            filename = args[1]

        process_all_loans(filename)

    except Exception as e:
        log.error(e)