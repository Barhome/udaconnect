FROM python:3.8

WORKDIR .

RUN pip install requests

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .

CMD ["python", "app/grpcserver.py"]