from models import LoanAssignment, FacilityYield
from utils import *
import pandas


class LoanProcessor(object):

    def __init__(self, facilities, covenants):
        self.facilities = facilities
        self.covenants = covenants
        self._facility_yields = []
        self.log = get_logger(__name__)

    def process_loan(self, loan):
        try:
            facility_id, interest_rate = self._find_facility(loan)

            if not facility_id:
                return

            loan_assignment = self._get_loan_assignment(loan, facility_id, interest_rate)
            self._add_to_facility_yield(loan_assignment)

        except Exception as e:
            self.log.error(e)

        return loan_assignment

    def get_facility_yields(self):

        if not self._facility_yields:
            return

        df = pandas.DataFrame(self._facility_yields, columns=['facility_id', 'expected_yield'])
        aggr = df.groupby(['facility_id']).sum()

        facility_yields = []
        for item in aggr.iterrows():

            facility_yield = FacilityYield()
            facility_yield.facility_id = item[0]
            facility_yield.expected_yield = int(item[1].values[0])
            facility_yields.append(facility_yield)

        return facility_yields

    # =====================
    # PRIVATE FUNCTIONS
    # =====================
    def _add_to_facility_yield(self, loan_assignment):
        self._facility_yields.append([loan_assignment.facility_id, loan_assignment.expected_yield])

    def _get_loan_assignment(self, loan, facility_id, interest_rate):

        if not loan:
            return

        expected_yield = self._calculate_expected_yield(loan.default_likelihood,
                                                        loan.interest_rate,
                                                        loan.amount,
                                                        interest_rate)

        loan_asignment = LoanAssignment()
        loan_asignment.loan_id = loan.id
        loan_asignment.facility_id = facility_id
        loan_asignment.expected_yield = expected_yield

        return loan_asignment

    def _find_facility(self, loan):
        cheapest_interest = None
        found_facility = None

        for key, facility in self.facilities.items():

            if loan.amount <= facility.amount and loan.interest_rate >= facility.interest_rate:

                if self._verify_covenant(loan, facility):

                    interest = facility.interest_rate * loan.amount

                    if cheapest_interest is None or interest < cheapest_interest:
                        cheapest_interest = interest
                        found_facility = facility

        found_facility.amount -= loan.amount

        return found_facility.facility_id, found_facility.interest_rate

    def _verify_covenant(self, loan, facility):
        key = get_key(facility.bank_id, facility.facility_id)
        covenant = self.covenants.get(key)
        if not covenant:
            return False
        else:
            return loan.default_likelihood <= covenant.max_default_likelihood and \
                   loan.state not in covenant.banned_states

    def _calculate_expected_yield(self, default_likelihood, loan_interest_rate, loan_amount, facility_interest_rate):

        expected_yield = (1 - default_likelihood) * loan_interest_rate * loan_amount \
                         - default_likelihood * loan_amount \
                         - facility_interest_rate * loan_amount

        return expected_yield