FROM python:3.13-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src /usr/src/app

ENV PYTHONPATH=/usr/src/app/main

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "main"]