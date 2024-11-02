import logging

from dotenv import load_dotenv

from artwork import ArtworkDataPipeline


logging.basicConfig(
    filename='logs/elt_pipeline.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


load_dotenv()


def main():
    artwork_processor = ArtworkDataPipeline()

    logging.info('Activate ELT pipeline...')
    artwork_processor.activate_pipeline()


if __name__ == "__main__":
    main()
