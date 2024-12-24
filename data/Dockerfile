FROM python:3.12-bookworm

RUN apt update

WORKDIR /cali
COPY . ./data

RUN pip install --no-cache -r data/requirements.txt

ENV PYTHONPATH="/cali"

CMD ["python", "data/run_pipeline.py"]
