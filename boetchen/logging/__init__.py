import logging
import logging.config

from importlib.resources import files

from typing import Dict
from pathlib import Path
import json


def __get_dict() -> Dict[str, Dict | str]:
    def is_config_file(p: Path):
        return p.name == "config.json"

    fs = files(__name__)
    config_files = tuple(filter(is_config_file, fs.iterdir()))

    if not config_files or len(config_files) > 1:
        raise FileNotFoundError("`config.json` not found")

    config_file = config_files[0]
    with config_file.open() as f:
        d = json.load(f)
    return d


def load_config():
    p = Path("logs/")
    if not p.exists():
        p.mkdir()
    try:
        log_config = __get_dict()
        logging.config.dictConfig(log_config)
    except FileNotFoundError:
        # config.json does not exist, use fallback config
        logging.basicConfig(
                level=logging.DEBUG,
                format="$(asctime)s %(message)s",
                handlers=[
                    logging.FileHandler("logs/fallback.log"),
                    logging.StreamHandler()
                ]
        )

