FROM python:3.12-alpine3.20

WORKDIR /cali

COPY . .
RUN pip install --no-cache -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
