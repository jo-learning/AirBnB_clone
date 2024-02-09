#!/usr/bin/python3
"""Defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """City.

    Attributes:
        state_id (str): state id.
        name (str): name of city.
    """

    state_id = ""
    name = ""
