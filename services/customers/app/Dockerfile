FROM python:3.10-slim

ENV SQLALCHEMY_DATABASE_URI postgresql://postgres:sadFrhn12<3@/lms_db?host=/cloudsql/clear-arbor-382814:europe-west6:bravos-lms/

RUN apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
    netcat-openbsd \
    && apt-get -q clean

RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 6061

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6061"]
