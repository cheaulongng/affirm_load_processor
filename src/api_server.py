from flask import Flask
from flask_restful import Api
from api.loans_api import LoansApi
from api.facilities_api import FacilitiesApi
from services.helper import load_finance_data

app = Flask(__name__)
api = Api(app)

# Load facilities, covenants data
load_finance_data(path='data_files')

# Define api route
api.add_resource(LoansApi, '/api/v1/loans')
api.add_resource(FacilitiesApi, '/api/v1/facilities')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)