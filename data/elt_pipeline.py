import logging

from dotenv import load_dotenv

from artwork import ArtworkDataPipeline


logging.basicConfig(
    filename='data/elt_pipeline.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


load_dotenv()


def main():
    artwork_processor = ArtworkDataPipeline()
    artwork_processor.activate_pipeline()


if __name__ == "__main__":
    main()
