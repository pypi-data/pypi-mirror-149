import logging
from typing import Optional

import yaml
import click
from box import Box

from elasticcsv import elastic_csv

logger = logging.getLogger(__name__)
config: Optional[Box] = None


@click.group()
def cli():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        level="WARNING"
    )
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    logging.getLogger("elasticcsv").setLevel(logging.DEBUG)
    global config
    logger.info("Loading connection.yaml file")
    with open("./connection.yaml") as conn_file:
        conn_d = yaml.load(conn_file, Loader=yaml.FullLoader)
        config = Box(conn_d, box_dots=True)
        if not config:
            logger.critical(f"Can't load csv into elastic without 'connection.yaml' config file")
            exit(1)
        logger.debug(config)


@cli.command()
@click.option("--csv", type=click.Path(exists=True), help="CSV File", required=True)
@click.option("--sep", type=click.STRING, help="CSV field sepator", required=True)
@click.option("--index", type=click.STRING, help="Elastic Index", required=True)
def load_csv(csv: str, index: str, sep: str):
    """Loads csv to elastic index"""
    logger.info(f"Loading file: {csv}")
    conn_config = Box(config.elastic_connection)
    elastic_csv.load_csv(config=conn_config, csv_file_name=csv, index=index, delimiter=sep)


if __name__ == "__main__":
    cli()
