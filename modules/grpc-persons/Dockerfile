FROM python:3.7-alpine

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 5005

COPY . .

CMD ["python", "grpcserver.py"]