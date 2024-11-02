from dependency_injector import containers, providers
from meili.meilisearch_utils import SearchInit, SearchAPI, make_documents


class Container(containers.DeclarativeContainer):

    documents_provider = providers.Factory(make_documents)
    search_init = providers.Singleton(SearchInit)
    search_api = providers.Factory(SearchAPI, c_index=search_init().index)
