FROM python:3.9
RUN pip install paramiko
RUN mkdir /service
WORKDIR /service
ADD . /service
CMD ["python", "/service/change_design.py"]
