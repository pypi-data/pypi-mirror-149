import logging
import time
from typing import Dict, Optional, List, Literal, Any, Union, Iterator
from datetime import datetime

from box import Box
from elasticsearch import Elasticsearch, ElasticsearchException, RequestsHttpConnection
from elasticsearch.helpers import streaming_bulk, scan
from tqdm import tqdm


logger = logging.getLogger(__name__)


class MyConnection(RequestsHttpConnection):
    def __init__(self, *args, **kwargs):
        proxies = kwargs.pop('proxies', {})
        super(MyConnection, self).__init__(*args, **kwargs)
        self.session.proxies = proxies


class ElasticWrapper(object):
    """Wrapper for Elasticsearch objects. Contains a list of Elasticsearch objects (one is default).
    Wraps:
        queries:
        index operations:
        bulk operations:
    """

    ELASTICSEARCH_TIMEOUT = 80
    DEFAULT_QUERY_SIZE = 10000
    DEFAULT_QUERY_CHUNK_SIZE = 5000

    def __init__(self, conn_conf: Box):
        """
        ElasticWrapper
        :param conn_conf: Box instance with connection info
        """
        logger.debug(conn_conf)
        self._proxies = conn_conf.proxies
        self._connection = self._get_connection(conn_conf)
        ElasticWrapper._shared_state = self.__dict__
        logger.info("ElasticWrapper initialized")

    @classmethod
    def get_client(cls, conn_conf: Box):
        return cls(conn_conf=conn_conf)

    def __repr__(self):
        return (f"<ElasticWrapper(connection={self._connection}, "
                f"proxies: {self._proxies})>")

    def __del__(self):
        """Close Elasticsearch connections when destroy"""
        if self._connection:
            self._connection.close()

    def _get_connection(self, conn_conf: Box) -> Elasticsearch:
        elastic_url: str = (
            f"http://{conn_conf.user}:{conn_conf.password}"
            f"@{conn_conf.node}:{conn_conf.port}"
        )
        if self._proxies:
            es = Elasticsearch(
                [elastic_url], connection_class=MyConnection, proxies=self._proxies
            )
        else:
            es = Elasticsearch([elastic_url])
        return es

    # ********
    # * BULK *
    # ********

    @staticmethod
    def _generate_actions(dataset):
        for element in dataset:
            yield element

    def bulk_dataset(
            self,
            data_iterator: Iterator[dict],
            index: str):
        """
        Función: bulk_dataset
        Descripción: Ingesta Dataset en formato array de objetos Json en elasticsearch

        :param data_iterator: Array de documentos ha realizar bulk en elasticsearch (Formato: [{..},{..},...])
        :param index: indice sobre el que se van a ingestar los datos
        :returns: ElasticJobResult
        """
        logger.info(f"Connection to Elasticsearch : {self._connection}")
        progress = tqdm(unit="docs")
        successes = fails = 0
        action = None
        try:
            for ok, action in streaming_bulk(
                    client=self._connection,
                    index=index,
                    actions=data_iterator,
                    raise_on_exception=True,
                    raise_on_error=True,
                    chunk_size=1000,
                    yield_ok=True
            ):
                if ok:
                    successes += 1
                else:
                    fails += 1

                progress.update(1)
        except ElasticsearchException as ee:
            logger.error(f"Action: {ee.args}, {action if action else None}")
        progress.close()
        logger.info("Documentos indexados: %d", successes)
        logger.warning(f"Documents not indexed: {fails}")

    @staticmethod
    def _result_from_generator(es_generator: Iterator) -> dict:
        hits = []
        tick = time.perf_counter_ns()
        for element in es_generator:
            hits.append(element)

        tock = time.perf_counter_ns()
        res = {
            "took": tock - tick,
            "hits": {
                "hits": hits,
                "total": {"value": len(hits), "relation": "eq"}
            }
        }
        return res
