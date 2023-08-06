import logging
from datetime import datetime, date
from typing import Iterator, List, Any, Dict
import pandas as pd
import pytz
from box import Box
from tqdm import tqdm

from elasticcsv.elastic_wrapper import ElasticWrapper

logger = logging.getLogger(__name__)


def load_csv(config: Box, csv_file_name: str, index: str, delimiter: str, logic_date: date = date.today()):
    """Main process to load csv to elastic
    :param config: Dictionary with elasctic connection data
    :param csv_file_name: csv file path
    :param index: index name (_index)
    :param delimiter: csv delimiter
    :param logic_date:
    """
    parent_data: bool = config.elastic_index.data_format.parent_data_object
    csv_iterator = _csv_reader(filepath=csv_file_name, delimiter=delimiter, logic_date=logic_date,
                               transform_to_data=parent_data)
    e_wrapper = ElasticWrapper(config.elastic_connection)
    e_wrapper.bulk_dataset(data_iterator=csv_iterator, index=index)


def _csv_reader(
        filepath: str,
        fields: List[str] = None,
        delimiter: str = None,
        chunk_size: int = 10000,
        logic_date: date = date.today(),
        transform_to_data: bool = True
) -> Iterator[dict]:
    """Returns an iterator of dicts

    :param filepath:
    :param fields:
    :param delimiter:
    :param chunk_size:
    :param logic_date:
    :param transform_to_data:
    :return:
    """
    fields = fields if fields else None
    tz = pytz.timezone('Europe/Madrid')
    ts: str = datetime.now(tz=tz).isoformat()  # strftime("%Y-%m-%dT%H:%M:%S")
    date_str = logic_date.isoformat() + "T00:00:00"

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
        chunk["@timestamp"] = ts
        chunk["date"] = date_str
        # chunk = chunk.applymap(str)
        for d in chunk.to_dict("records"):
            if transform_to_data:
                yield _transform_to_data_struct(d)
            else:
                yield d


def _set_timestamp(registro: Dict[str, Any], **kwargs):
    """set timestamp

    :param registro:
    """
    ts = kwargs.get("ts")
    registro["@timestamp"] = ts


def _transform_to_data_struct(reg: Dict[str, str]) -> Dict[str, Any]:
    data = copy_elastic_properties(reg, system=False)
    props = copy_elastic_properties(reg, system=True)
    new_reg = {"data": data}
    new_reg.update(**props)
    return new_reg


def copy_elastic_properties(registro: Dict[str, str], system: bool) -> Dict[str, str]:
    if not system:
        keys = list(filter(lambda k: k[0] not in ["_", "@"] and k not in ["date"], list(registro.keys())))
    else:
        keys = list(filter(lambda k: k[0] in ["_", "@"] or k in ["date"], list(registro.keys())))
    new_reg: Dict[str, str] = {k: registro[k] for k in keys if
                               isinstance(registro[k], str) or
                               isinstance(registro[k], int) or
                               isinstance(registro[k], float)}
    return new_reg
