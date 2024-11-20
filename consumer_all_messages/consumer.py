import json
from kafka import KafkaConsumer
from pymongo import MongoClient

MONGO_URI = 'mongodb://admin:1234@mongodb:27017/'
DB_NAME = 'emails'
COLLECTION_NAME = "all_messages"

def get_mongo_connection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection

consumer = KafkaConsumer(
    'all_message',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='all_message_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for mess in consumer:
    message = mess.value
    collection = get_mongo_connection()
    collection.insert_one(message)
    print(f"Stored all message: {message}")