FROM python:3.7-alpine

WORKDIR .

RUN apk add linux-headers

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .

CMD ["python", "grpcserver.py"]