'''
For convenience we put all models into a single file. We could separate into separate files
'''


class Bank(object):
    def __init__(self):
        self.bank_id = None
        self.bank_name = None


class Facility(object):
    def __init__(self):
        self.bank_id = None
        self.facility_id = None
        self.amount = None
        self.interest_rate = None
        self.default_likelihood = None
        self.state = None


class Covenant(object):
    def __init__(self):
        self.bank_id = None
        self.facility_id = None
        self.max_default_likelihood = None
        self.banned_states = []


class Loan(object):
    def __init__(self):
        self.loan_id = None
        self.amount = None
        self.interest_rate = None
        self.default_likelihood = None
        self.state = None


class LoanAssignment(object):
    def __init__(self):
        self.loan_id = None
        self.facility_id = None
        self.expected_yield = None


class FacilityYield(object):
    def __init__(self):
        self.facility_id = None
        self.expected_yield = None