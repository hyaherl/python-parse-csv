# python:3.9의 이미지로 부터
FROM python:3.9
RUN pip install pandas

RUN mkdir /curate
RUN mkdir /curate/input
RUN mkdir /curate/output

COPY ./curate.sh /curate

WORKDIR /usr/app
COPY ./parseCsvToJson.py .

ENTRYPOINT ["python", "parseCsvToJson.py"]