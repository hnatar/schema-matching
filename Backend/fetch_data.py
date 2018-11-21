#!/usr/bin/env python3

import pymongo
import argparse

def get_data(db, col, field):
    client = pymongo.MongoClient( f'mongodb://127.0.0.1:27018/' )
    collection = client[db][col]
    query = {}
    projection = {field: '1'}
    if field != '_id':
        projection['_id'] = '0'
    for x in collection.find(query, projection):
        yield str(x.get(field, 'undefined'))

def write_to_file(db, col, field):
    File = 'FieldData/MONGO_' + '_'.join([db,col,field]) + '.txt'
    with open(File, 'w') as f:
        for line in get_data(db, col, field):
            if line == 'undefined':
                continue
            f.write(line + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Utility to extract values associated with specified field from MongoDB database')
                    
    parser.add_argument('--field', help="Field to search for", required=True)
    parser.add_argument('--host', help='MongoDB host instance', required=True)
    parser.add_argument('--port', help='MongoDB port number', required=True)
    parser.add_argument('--db', help='MongoDB database', required=True)
    parser.add_argument('--col', help='MongoDB collection', required=True)
    args = parser.parse_args()

    field = args.field or 'firstname'
    host = args.host or '127.0.0.1'
    port = args.port or 27018
    db = args.db or 'EDM'
    col = args.col or 'account'

    write_to_file(db, col, field)
