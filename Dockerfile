FROM python:alpine3.16

COPY application.py requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python", "application.py" ]


