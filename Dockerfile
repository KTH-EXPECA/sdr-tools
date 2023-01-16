FROM python:3.9
RUN pip install paramiko
ENV DESIGN='mango'
ENV SDR='sdr-01'
RUN mkdir /service
WORKDIR /service
ADD . /service
CMD ["python", "/service/test.py"]
