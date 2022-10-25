# python:3.9의 이미지로 부터
FROM python:3.8-slim-buster
RUN pip install pandas

RUN mkdir -p /curate/input
RUN mkdir -p /curate/output

WORKDIR /curate
COPY ./curate.sh .
COPY ./env.sh .
COPY ./parseCsvToJson.py .

CMD ["/bin/sh", "-c", "/bin/bash"]