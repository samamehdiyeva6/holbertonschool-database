#!/usr/bin/env python3
"""
This module contains the function list_all that lists all documents in a collection
"""


import pymongo


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    """
    if mongo_collection is None:
        return []
    return list(mongo_collection.find())
