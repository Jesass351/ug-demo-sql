FROM python:3.9-slim

WORKDIR /app

RUN pip install flask==2.0.1 mysql-connector-python==8.0.26 Werkzeug==2.3.4
RUN pip install Cmake setuptools wheel
RUN pip install --only-binary :all: greenlet
RUN pip install waitress


COPY ./app .

CMD waitress-serve --host 0.0.0.0 --port 8000 app:app
