from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import logging
import json


@dataclass
class UserToken:
    """
    :since:3.0.0
    :new_feature:
    """

    name: Optional[str] = None
    description: Optional[str] = None
    key: str = ""

    @staticmethod
    def parse_api_token_json(token_file: str) -> UserToken:
        logging.info("Parsing api token json file...")
        with open(token_file) as file:
            data = json.load(file)
        return UserToken(**data)
