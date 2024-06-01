#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from typing import Literal
from pydantic import BaseModel, Field


class AvroFormat(BaseModel):
    'This connector utilises <a href="https://fastavro.readthedocs.io/en/latest/" target="_blank">fastavro</a> for Avro parsing.'

    class Config:
        title = "Avro"

    filetype: Literal["avro"] = "avro"
