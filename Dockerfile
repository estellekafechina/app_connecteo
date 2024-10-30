FROM python:3.11.9-bookworm AS build

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app-connecteo /app-connecteo

WORKDIR /app-connecteo

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]