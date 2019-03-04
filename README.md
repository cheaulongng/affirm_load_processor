# Affirm Loan Processor

This program will consume loans from the stream (loans.csv) and assign each loan to a funding facility while
respecting each facility's covenants. Once the program finishes the process, it will generate two output files -
assignments.csv and yields.csv


```
|---src/                        # Source codes      
|   |---api/                    # API views folder   
|   |---common/                 # Common utility    
|   |---data_files/             # Finance data file folder
|       |---small/              # Small dataset files
|       |---banks.csv           # Bank datafile
|       |---covenants.csv       # Facility covenant datafile
|       |---facilities.csv      # Funding facilities datafile
|       |---loans.csv           # Loan datafile
|   |---models/                 # Models folder
|   |---services/               # Services folder
|   |---tests/                  # Unit testing files
|   |---output/                 # Output files. assignments.csv, yields.csv
|---docker-compose              # Docker compose to run api
|---Dockerfile                  # Dockerfile to build api image
|---README.md                   
|---requirements.txt            #Requirements to install python libraries
```

------------------------

# How to run the program?

## Run "process_loans.py" script

Change the working directory to "src", then run command below:

```
python process_loans.py data_files/loans.csv

```

It will generate two output files: assignments.csv, yields.csv


Example:

```
ng-mac:src cheau$ python process_loans.py data_files/small/loans.csv
2019-03-03 00:01:41,587 - INFO - START Processing Loans
2019-03-03 00:01:41,587 - INFO - Process loan_id: 1, funded facility_id: 1
2019-03-03 00:01:41,587 - INFO - Process loan_id: 2, funded facility_id: 2
2019-03-03 00:01:41,587 - INFO - Process loan_id: 3, funded facility_id: 1
2019-03-03 00:01:41,587 - INFO - Generate assignments.csv
2019-03-03 00:01:41,587 - INFO - Generate yields.csv
2019-03-03 00:01:41,588 - INFO - END Processing Loans

```


## Run API Server in Docker

We can also run the Loan API server. This is a simple demo to process loan thru API, and get the facility yields

To run the API thru docker-compose

```
docker-compose up

```


If successfully run, we should see example below:

```
ng-mac:src cheau$ docker-compose up
loan_api_local is up-to-date
Attaching to loan_api_local
loan_api_local |  * Serving Flask app "api_server" (lazy loading)
loan_api_local |  * Environment: production
loan_api_local |    WARNING: Do not use the development server in a production environment.
loan_api_local |    Use a production WSGI server instead.
loan_api_local |  * Debug mode: on
loan_api_local | 2019-03-03 07:42:03,495 - INFO -  * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
loan_api_local | 2019-03-03 07:42:03,496 - INFO -  * Restarting with stat
loan_api_local | 2019-03-03 07:42:03,640 - WARNING -  * Debugger is active!
loan_api_local | 2019-03-03 07:42:03,641 - INFO -  * Debugger PIN: 197-970-533
loan_api_local | 2019-03-03 07:58:05,214 - INFO - 172.25.0.1 - - [03/Mar/2019 07:58:05] "POST /api/v1/loans HTTP/1.1" 200 -
loan_api_local | 2019-03-03 07:58:09,110 - INFO - 172.25.0.1 - - [03/Mar/2019 07:58:09] "POST /api/v1/loans HTTP/1.1" 200 -
loan_api_local | 2019-03-03 07:58:18,343 - INFO - 172.25.0.1 - - [03/Mar/2019 07:58:18] "POST /api/v1/loans HTTP/1.1" 200 -

```

Methods:

POST  http://0.0.0.0:8080/api/v1/loans

Example Payload:
```
{
    "loan_id": 1,
    "amount": 10000,
    "interest_rate": 0.15,
    "default_likelihood": 0.02,
    "state": "MO"
}

```


GET http://0.0.0.0:8080/api/v1/facilities


Example Response:

```
{
    "data": [
        {
            "facility_id": 1,
            "expected_yield": 98
        }
    ]
}

```




