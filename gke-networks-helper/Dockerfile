FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN pip install requests google-api-python-client oauth2client

RUN mkdir /code/
WORKDIR /code/
COPY [ "gke-master-authorized-network-add.py", "gke-master-authorized-network-delete.py", "/code/" ]
