from flask import Flask, jsonify, request
from kafka import KafkaProducer
import json

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def rout_emails(data):
    sentences = [sentence.lower() for sentence in data['sentences']]
    if 'hostage' in sentences and 'explos' in sentences:
        return 'hostage', 'explos', 'all'
    if 'hostage' in sentences:
        return 'hostage', 'all'
    elif 'explos' in sentences:
        return 'explos', 'all'
    else:
        return tuple('all')

def send_emails(data):
    topics = rout_emails(data)
    for topic in topics:
        producer.send(f'{topic}_message', value=data)

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Received'}), 200

@app.route('/api/email', methods=['POST'])
def get_email():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Incorrect data'}), 400
        if 'sentences' not in data:
            return jsonify({'error': 'Incorrect format data'}), 400
        send_emails(data)
        return jsonify({'message': 'Received'}), 200

    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 500


if __name__ == "__main__":
    app.run(debug=True)