FROM python:3.8

COPY . /app

WORKDIR /app

RUN bash install_req_file.sh requirements.txt
RUN bash install_req_file.sh requirements.app

CMD uvicorn akerbp.mlops.gc.app:app --host 0.0.0.0 --port $PORT
