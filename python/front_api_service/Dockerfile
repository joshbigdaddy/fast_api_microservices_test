FROM python:3.8
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN python3 -m pip install -r requirements.txt
RUN export TEST="True"
RUN pytest tests
RUN export TEST="False"
CMD ["uvicorn","front_api:app","--host","0.0.0.0","--port","80"]
#uvicorn front_api:app --host 0.0.0.0 --port 80
# FOR TESTS TO RUN -- MONGODB CONTAINER MUST BE ON