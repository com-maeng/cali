import json

from .config import Config, create_documents
from .search import Search


def main():
    conf = Config()

    hanjas = ["日 날 일", "月 달 월", "火 불 화"]

    docs = create_documents(hanjas)
    conf.add_docs(docs)
    conf.add_filter()

    sch = Search(conf)
    result = sch.search("불", "yeseo")

    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
