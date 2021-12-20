FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get install -y git

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /home/src

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "./entrypoint.sh" ]