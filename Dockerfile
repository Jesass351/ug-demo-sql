FROM python:3.9-slim

WORKDIR /app

RUN pip install flask==2.0.1 mysql-connector-python==8.0.26

COPY ./app .

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
