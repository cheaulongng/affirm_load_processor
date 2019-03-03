FROM python:3

WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
WORKDIR /usr/app/src

CMD ["python", "api_server.py"]