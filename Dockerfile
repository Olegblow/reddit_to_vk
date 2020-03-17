FROM python:3.7

COPY ./setup.py setup.py
COPY ./app /app
RUN python setup.py develop

