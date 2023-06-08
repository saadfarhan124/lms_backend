FROM python:3.10-slim


RUN apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
    netcat \
    && apt-get -q clean

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6061

CMD ["python", "main.py"]