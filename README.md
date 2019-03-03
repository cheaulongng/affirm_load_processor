#Affirm Loan Processor

This program will consume loans from the stream (loan.csv) and assign each loan to a funding facility while
respecting each facility's covenants. Once the program finishes the process, it will generate two output files
assignments.csv, and yields.csv


```
|---src/                        #Source codes              
|   |---files/                  #Finance data file folder
|       |---small/              #Small dataset files
|       |---banks.csv           #Bank datafile
|       |---covenants.csv       #Facility covenant datafile
|       |---facilities.csv      #Funding facilities datafile
|       |---loans.csv           #Loan datafile
|---output/                     #Output file folder    
|   |---assignments.csv         #Loan assignments file
|   |---yields.csv              #Facility yields file
|---Dockerfile                  #Dockerfile to run the program
|---README.md                   
|---requirements.txt            #Requirements to install python libraries
```

------------------------

# How to run the program?
Two ways to run the program:

## Docker
We can run the program using docker. Running command below will build a docker image and run the program.
It will take the default "loans.csv" from files/loans.csv; this is the large dataset file. 
The output files "assignments.csv", "yields.csv" will be generated in "output" folder"

Using cat allows to show the contents of the output files.

```
docker run processor cat output/assignments.csv output/yields.csv 

```

The approach can be enhanced later by using input from the host, but this involves mounting the volume.


## Command

```
cd src

python process_loans.py files/loans.csv

```

