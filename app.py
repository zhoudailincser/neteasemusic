from pymongo import MongoClient
from flask import Flask, jsonify

# 连接数据库
client = MongoClient('127.0.0.1', 27017)
db = client.neteasemusicdata
data = db.data

data.update_many({"song":""}, {"$unset": {"outerchain": ""}})
