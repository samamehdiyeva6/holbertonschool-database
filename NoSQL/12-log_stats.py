#!/usr/bin/env python3
"""
This module contains the function insert_school that inserts a new document in a collection
"""

import pymongo


def log_stats():
    """
    Connect to a MongoDB database and print the number of documents in the collection
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    collection = client.logs.nginx

    count = collection.count_documents({})
    print(f"Number of documents in the collection: {count}")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    get_status_count = collection.count_documents(
        {
            "method": "GET",
            "path": "/status"
        })
    print(f"{get_status_count} status check")

if __name__ == "__main__":
    log_stats()
