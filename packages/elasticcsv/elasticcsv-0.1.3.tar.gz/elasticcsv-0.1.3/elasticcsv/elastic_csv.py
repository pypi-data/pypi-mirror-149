from typing import Iterator, List
import pandas as pd
from box import Box
from tqdm import tqdm

from elasticcsv.elastic_wrapper import ElasticWrapper


def load_csv(config: Box, csv_file_name: str, index: str, delimiter: str):
    """Main process to load csv to elastic
    :param config: Dictionary with elasctic connection data
    :param csv_file_name: csv file path
    :param index: index name (_index)
    :param delimiter: csv delimiter
    """
    csv_iterator = _csv_reader(filepath=csv_file_name, delimiter=delimiter)
    e_wrapper = ElasticWrapper(config)
    e_wrapper.bulk_dataset(data_iterator=csv_iterator, index=index)


def _csv_reader(
        filepath: str,
        fields: List[str] = None,
        delimiter: str = None,
        chunk_size: int = 1000,
) -> Iterator[dict]:
    """Returns an iterator of dicts

    :param filepath:
    :param fields:
    :param delimiter:
    :param chunk_size:
    :return:
    """
    fields = fields if fields else None

    df_chunks = pd.read_csv(
        filepath_or_buffer=filepath,
        delimiter=delimiter,
        names=fields,
        header=0,
        chunksize=chunk_size,
        iterator=True
    )

    for chunk in tqdm(df_chunks, unit="chunk of lines"):
        if "" in chunk.columns:
            chunk.drop([''], axis=1, inplace=True)
        chunk.dropna(axis=1, how="all", inplace=True)
        chunk.fillna('', inplace=True)
        # chunk = chunk.applymap(str)
        for d in chunk.to_dict("records"):
            yield d
