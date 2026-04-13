#!/usr/bin/env python3
"""
This module contains the function insert_school that inserts a new document in a collection
"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection
    """
    if mongo_collection is None:
        return None
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
