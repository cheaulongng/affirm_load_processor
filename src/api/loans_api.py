from flask_restful import Resource
from flask import request
from http import HTTPStatus
from services.helper import get_loan_service
from models.models import Loan
from common.exceptions import DataValidationException
from common.utils import *


class LoansApi(Resource):

    def post(self):
        status = HTTPStatus.OK
        request_data = request.get_json(request)

        json_data = None

        try:
            svc = get_loan_service()

            loan = Loan()
            loan.loan_id = request_data.get('loan_id')
            loan.amount = request_data.get('amount')
            loan.interest_rate = request_data.get('interest_rate')
            loan.default_likelihood = request_data.get('default_likelihood')
            loan.state = request_data.get('state')

            # validate data
            if not loan.loan_id:
                raise DataValidationException('Missing loan_id')

            loan_assignment = svc.process_loan(loan)

            result = OrderedDict()
            result['loan_id'] = loan_assignment.loan_id
            result['facility_id'] = loan_assignment.facility_id
            result['expected_yield'] = to_int(loan_assignment.expected_yield)

            json_data = jsonify_standard_response(result)

        except DataValidationException as e:
            status = e.status_code
            json_data = get_error_response_data(e)

        except Exception as e:
            status = HTTPStatus.INTERNAL_SERVER_ERROR

        finally:
            return json_data, status



