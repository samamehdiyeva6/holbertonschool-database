#!/usr/bin/env python3
"""
This module contains the function insert_school that inserts a new document in a collection
"""


import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic
    """
    if mongo_collection is None:
        return []
    return list(mongo_collection.find({'topics': topic}))
