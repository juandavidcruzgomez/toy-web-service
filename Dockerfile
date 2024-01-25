FROM python:3.11

WORKDIR /var/web

ADD app .

RUN pip install -r requirements.txt

EXPOSE 8000

VOLUME ["models"]

CMD ["uvicorn", "--host 0.0.0.0", "main:app"]
