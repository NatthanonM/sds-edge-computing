FROM python:3.6-buster

WORKDIR /usr/src/app

COPY backend backend
COPY database/data database/data

WORKDIR /backend
RUN pip install -r requirements.txt

CMD ["python", "./main.py" ]

EXPOSE 5000