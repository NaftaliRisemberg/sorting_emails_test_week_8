from database import db_session
import json
from models import *
from kafka import KafkaConsumer


consumer = KafkaConsumer(
    'explos_message',
    bootstrap_servers='db_psql:5432',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='explosive_messages_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def change_order_sentences(sentences):
    priority_sentences = [sentence for sentence in sentences if "hostage" in sentence or "explos" in sentence]
    other_sentences = [sentence for sentence in sentences if sentence not in priority_sentences]
    sentc_string = " ".join(priority_sentences + other_sentences)
    return sentc_string

for email in consumer:
    email_data = json.loads(email.value)
    print(f"received message: {email_data['email']}")

    location_data = email_data.get('location')
    location = Location(latitude=location_data['latitude'],
                        longitude=location_data['longitude'],
                        city=location_data['city'],
                        country=location_data['country'])

    device_info_data = email_data.get('device_info')
    device_info = DeviceInfo(browser=device_info_data['browser'],
                             os=device_info_data['os'],
                             device_id=device_info_data['device_id'])

    email = Email(username=email_data['username'],
                        email=email_data['email'],
                        ip_address=email_data['ip_address'],
                        created_at=email_data['created_at'],
                        location=location,
                        device_info=device_info)

    sentences = Sentence(sentences=change_order_sentences(email_data['sentences']))

    try:
        db_session.add(email)
        db_session.add(location)
        db_session.add(device_info)
        db_session.add(sentences)
        db_session.commit()

        print("Data inserted successfully!")

    except Exception as e:
        db_session.rollback()
        print(f"Error inserting data: {e}")
