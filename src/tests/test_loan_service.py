from unittest import TestCase
from services.finance_data import load_facilities, load_covenants
from services.loan_service import LoanService
from models.models import Loan


class TestLoanService(TestCase):

    '''
    TODO: Add more unit tests

    '''

    facilities = None
    covenants = None
    loan_service = None

    @classmethod
    def setUpClass(self):
        self.prepare_data(self)

    def prepare_data(self):
        self.facilities = load_facilities()
        self.covenants = load_covenants()
        self.loan_service = LoanService(self.facilities, self.covenants)

    # =================
    # Test Cases
    # =================

    def test_process_none_loan(self):
        assignment = self.loan_service.process_loan(None)
        self.assertIsNone(assignment)

    def test_process_loan(self):
        loan = Loan()
        loan.loan_id = 1
        loan.amount = 10000
        loan.interest_rate = 0.15
        loan.default_likelihood = 0.05
        loan.state = 'CA'

        assignment = self.loan_service.process_loan(loan)

        self.assertEqual(1, assignment.loan_id)
        self.assertEqual(2, assignment.facility_id)
