#!/usr/bin/env python3
"""
This module contains the function insert_school that inserts a new document in a collection
"""


import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document based on the name
    """
    if mongo_collection is None:
        return None
    result = mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
