FROM python:3.12-bookworm

RUN <<EOF
apt update && \
apt install -y tesseract-ocr-chi-sim tesseract-ocr-chi-sim-vert tesseract-ocr-chi-tra tesseract-ocr-chi-tra-vert
EOF

WORKDIR /cali
COPY . ./data

RUN pip install --no-cache -r data/requirements.txt

ENV PYTHONPATH="/cali"

CMD ["python", "data/run_pipeline.py"]
