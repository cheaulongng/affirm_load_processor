from services.loan_service import LoanService
from services.finance_data import *


_loan_processor = None
_facilities_data = None
_covenants_data = None


def load_finance_data(path):
    global _facilities_data
    global _covenants_data

    if not _facilities_data:
        _facilities_data = load_facilities(path)

    if not _covenants_data:
        _covenants_data = load_covenants(path)


def get_loan_service(path=None):
    global _loan_processor

    if not _loan_processor:
        _loan_processor = LoanService(_facilities_data, _covenants_data)

    return _loan_processor


