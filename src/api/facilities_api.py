from flask_restful import Resource
from http import HTTPStatus
from services.helper import get_loan_service
from common.utils import *


class FacilitiesApi(Resource):
    def get(self):
        status = HTTPStatus.OK

        try:
            svc = get_loan_service()

            facility_yields = svc.get_facility_yields()

            result_list = []
            for key, facility_yield in facility_yields.items():
                result = OrderedDict()
                result['facility_id'] = facility_yield.facility_id
                result['expected_yield'] = to_int(facility_yield.expected_yield)

                result_list.append(result)

            json_data = jsonify_standard_response(result_list)

        except Exception as e:
            status = HTTPStatus.INTERNAL_SERVER_ERROR

        finally:
            return json_data, status


