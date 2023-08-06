import csv
import logging
import math
from datetime import datetime, date
from typing import Iterator, List, Any, Dict, Generator
import pandas as pd
import pytz
from box import Box
from tqdm import tqdm

from elasticcsv.elastic_wrapper import ElasticWrapper

logger = logging.getLogger(__name__)

DEFAULT_CSV_WRITE_CHUNK_SIZE = 50000


def download_csv(
    config: Box,
    csv_file_name: str,
    index: str,
    delimiter: str,
):
    """Main process to load csv to elastic
    :param config: Dictionary with elasctic connection data
    :param csv_file_name: csv file path
    :param index: index name (_index)
    :param delimiter: csv delimiter
    """
    e_wrapper = ElasticWrapper(config.elastic_connection)
    es_iterator = e_wrapper.scan(index=index)
    _write_csv(es_iterator, csv_file_name=csv_file_name, delimiter=delimiter)


def load_csv(
    config: Box,
    csv_file_name: str,
    index: str,
    delimiter: str,
    logic_date: date = date.today(),
):
    """Main process to load csv to elastic
    :param config: Dictionary with elasctic connection data
    :param csv_file_name: csv file path
    :param index: index name (_index)
    :param delimiter: csv delimiter
    :param logic_date:
    """
    parent_data: bool = config.elastic_index.data_format.parent_data_object
    csv_iterator = _csv_reader(
        filepath=csv_file_name,
        delimiter=delimiter,
        logic_date=logic_date,
        transform_to_data=parent_data,
        count_lines=True
    )
    e_wrapper = ElasticWrapper(config.elastic_connection)
    e_wrapper.bulk_dataset(data_iterator=csv_iterator, index=index)


def _csv_reader(
    filepath: str,
    delimiter: str = None,
    chunk_size: int = 10000,
    logic_date: date = date.today(),
    transform_to_data: bool = True,
    count_lines: bool = False
) -> Generator[dict, None, None]:
    """Returns an iterator of dicts

    :param filepath:
    :param delimiter:
    :param chunk_size:
    :param logic_date:
    :param transform_to_data:
    :param count_lines: file line count before iteration process
    :return:
    """
    logger.debug(f"Loading generator for filename: {filepath}")
    tz = pytz.timezone("Europe/Madrid")
    ts: str = datetime.now(tz=tz).isoformat()  # strftime("%Y-%m-%dT%H:%M:%S")
    date_str = logic_date.isoformat() + "T00:00:00"

    total_chunks = None
    if count_lines:
        total_lines = _count_lines(filepath)
        total_chunks = math.ceil(total_lines / chunk_size)

    df_chunks = pd.read_csv(
        filepath_or_buffer=filepath,
        delimiter=delimiter,
        names=None,
        header=0,
        chunksize=chunk_size,
        iterator=True,
    )

    for chunk in tqdm(df_chunks, unit=f" ({chunk_size} lines group)", total=total_chunks):
        if "" in chunk.columns:
            chunk.drop([""], axis=1, inplace=True)
        chunk.dropna(axis=1, how="all", inplace=True)
        chunk.fillna("", inplace=True)
        chunk["@timestamp"] = ts
        chunk["date"] = date_str

        for d in chunk.to_dict("records"):
            if transform_to_data:
                yield _transform_to_data_struct(d)
            else:
                yield d


def _write_csv(
        es_iterator: Iterator[dict],
        csv_file_name: str,
        encoding: str = "utf-8",
        chunk_size: int = DEFAULT_CSV_WRITE_CHUNK_SIZE,
        delimiter: str = ";"):
    """

    :param es_iterator: elastic iterator returning hits
    :param csv_file_name: file to append hits as csv rows
    :param encoding:
    :param chunk_size:
    :return:
    """
    data = True
    first_chunk = True
    while data:
        dicts: List[dict] = []
        i = 0
        for i, hit in tqdm(enumerate(es_iterator),
                           desc=f"Download chunk of hits ({DEFAULT_CSV_WRITE_CHUNK_SIZE})",
                           unit=" hit"):
            # ! hit.get("_source")
            dicts.append(hit.get("_source"))
            if i >= chunk_size:
                break
        if i < chunk_size:
            data = False
        if not dicts:
            logger.debug(f"Nothing to write to csv_filename: {csv_file_name}")
        else:
            # flatten dict values (only one level) as key1.key11: value11
            if any([isinstance(value, dict) for value in list(dicts[0].values())]):
                dicts = list(map(_flatten_dict, dicts))

            with open(csv_file_name, "a", encoding=encoding) as f:
                headers = list((dicts[0].keys()))
                writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
                if first_chunk:
                    writer.writeheader()
                writer.writerows(dicts)
            first_chunk = False


def _flatten_dict(dct: dict) -> dict:
    new_fields = {}
    for k, v in list(dct.items()):
        if isinstance(v, dict):
            for kk, vv in list(v.items()):
                new_fields[".".join([k, kk])] = vv
        else:
            new_fields[k] = v
    return new_fields


def _transform_to_data_struct(reg: Dict[str, str]) -> Dict[str, Any]:
    data = copy_elastic_properties(reg, system=False)
    props = copy_elastic_properties(reg, system=True)
    new_reg = {"data": data}
    new_reg.update(**props)
    return new_reg


def copy_elastic_properties(registro: Dict[str, str], system: bool) -> Dict[str, str]:
    if not system:
        keys = list(
            filter(
                lambda k: k[0] not in ["_", "@"] and k not in ["date"],
                list(registro.keys()),
            )
        )
    else:
        keys = list(
            filter(lambda k: k[0] in ["_", "@"] or k in ["date"], list(registro.keys()))
        )
    new_reg: Dict[str, str] = {
        k: registro[k]
        for k in keys
        if isinstance(registro[k], str)
        or isinstance(registro[k], int)
        or isinstance(registro[k], float)
    }
    return new_reg


def _count_generator(raw_reader: callable) -> Generator[bytes, None, None]:
    b = raw_reader(1024*1024)
    while b:
        yield b
        b = raw_reader(1024 * 1024)


def _count_lines(filepath: str) -> int:
    """count lines of `filepath` file with good performance

    :param filepath:
    :return: Number of lines
    """
    with open(filepath, mode="rb") as f:
        # noinspection PyUnresolvedReferences
        generator = _count_generator(f.raw.read)
        count = sum(buffer.count(b'\n') for buffer in generator)
        return count
