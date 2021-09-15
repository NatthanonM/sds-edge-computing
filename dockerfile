FROM python:3.6-buster

WORKDIR /usr/src/app

COPY backend backend
COPY database/data database/data
COPY database/data.txt database/data.txt

WORKDIR /usr/src/app/backend
RUN pip install -r requirements.txt

CMD ["python", "./main.py" ]

EXPOSE 5000