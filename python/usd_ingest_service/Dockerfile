FROM python:3.8
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN python3 -m pip install -r requirements.txt
RUN python3 -m unittest tests/*
CMD ["python3","usd_ingest_service.py"]