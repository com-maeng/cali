#/bin/sh

export MEILI_MASTER_KEY=x0tii5RDPBcoP7PX  # Random 16 bytes base64 value
sh -c /bin/meilisearch &
MEILISEARCH_PID=$!

apk add python3=3.12.8-r1 py3-pip
pip install -r /cali/search_engine/requirements.txt --break-system-packages

export PYTHONPATH=/cali
python /cali/search_engine/run_init_config.py

kill $MEILISEARCH_PID  # Restart after initial settings
sh -c /bin/meilisearch
