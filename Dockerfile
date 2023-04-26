FROM python:3.9
RUN pip install paramiko
RUN mkdir /service
WORKDIR /service
ADD . /service
RUN chmod +x /service/entrypoint.sh
ENTRYPOINT ["/service/entrypoint.sh"]
