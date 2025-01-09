import logging

from search_engine.meili_customize.config import Config
from search_engine.meili_customize.config import create_documents, hanja_preprocessor


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


def main():
    logging.info('Meilisearch server connection...')
    conf = Config()

    logging.info('Hanja preprocessing...')
    hanjas = hanja_preprocessor()

    logging.info('Create indexed documents...')
    documents = create_documents(hanjas)

    logging.info('Add indexed documents, filtering define......')
    conf.add_docs(documents)


if __name__ == '__main__':
    main()
