import logging

from meili_customize.config import Config, create_documents, hanja_preprocessor


logging.basicConfig(
    filename='logs/search_initial.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
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
    conf.add_filter()


if __name__ == '__main__':
    main()
