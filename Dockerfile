FROM python:3.11-slim-buster
RUN pip install --upgrade pip
RUN pip cache purge
RUN apt-get update \
    && apt-get install -y --no-install-recommends
WORKDIR /task
# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .


