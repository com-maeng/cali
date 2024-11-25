import logging

from dotenv import load_dotenv

from pipelines.artwork import ArtworkDataPipeline
from pipelines.hanja import HanjaDataPipeline


logging.basicConfig(
    filename='data/logs/elt_pipeline.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


load_dotenv()


def main():
    artwork_data_pipeline = ArtworkDataPipeline()

    logging.info('Activate ELT pipeline...')
    artworks = artwork_data_pipeline.activate_pipeline()

    if not artworks:
        logging.info('새로 적재할 artwork가 없습니다.')
    else:
        hanja_data_pipeline = HanjaDataPipeline(artworks)
        hanja_data_pipeline.activate_pipeline()


if __name__ == "__main__":
    main()
