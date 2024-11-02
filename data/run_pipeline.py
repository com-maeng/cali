import logging

from dotenv import load_dotenv

from artwork import ArtworkDataPipeline
# from hanja import HanjaDataPipeline


logging.basicConfig(
    filename='logs/elt_pipeline.log',
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
    # 한자 데이터 적재 파이프라인 구현 시 활용될 코드
    # else:
    #     hanja_data_pipeline = HanjaDataPipeline(artworks)
    #     hanjas = hanja_data_pipeline.activate_pipeline()

    #     if not hanjas:
    #         logging.warning('Artwork에서 분리된 한자 이미지가 없습니다.')


if __name__ == "__main__":
    main()
