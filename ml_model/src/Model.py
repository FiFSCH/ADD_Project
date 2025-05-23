import os
import json
import joblib
import pika
import pandas as pd
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv

load_dotenv()

MODEL_INPUT = os.getenv('MODEL_INPUT', '../logistic_regression_add.pkl')
RABBITMQ_MODEL_INPUT_QUEUE = os.getenv('RABBITMQ_PROCESSOR_ML_QUEUE', 'processor_ml_processed_data')
RABBITMQ_ML_UPLOADER_QUEUE = os.getenv('RABBITMQ_ML_UPLOADER_QUEUE', 'ml_uploader_metrics_data')


def get_rabbitmq_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'rabbit-server'),
        port=int(os.getenv('RABBITMQ_PORT', '5672')),
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_USER', 'guest'),
            password=os.getenv('RABBITMQ_PASSWORD', 'guest')
        )))


def load_model():
    try:
        with open(MODEL_INPUT, 'rb') as file:
            model = joblib.load(file)
        print("[MODEL] Loaded model")
    except Exception as e:
        print(f"[MODEL ERROR] Failed to load model: {e}")
        model = None

    return model


def evaluate_model(model, batch_data):
    if isinstance(batch_data, dict):
        batch_data = [batch_data]

    df = pd.DataFrame(batch_data)

    X = df.drop(columns=['blueWin', 'matchId'])
    y_true = df['blueWin']

    y_pred = model.predict(X)
    accuracy = accuracy_score(y_true, y_pred)

    return accuracy


def start_model():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_MODEL_INPUT_QUEUE)
    channel.queue_declare(queue=RABBITMQ_ML_UPLOADER_QUEUE)

    model = load_model()

    print("[MODEL] Listening for data batch...")

    while True:
        _, _, body = channel.basic_get(queue=RABBITMQ_MODEL_INPUT_QUEUE, auto_ack=True)
        if not body:
            continue

        data = json.loads(body)
        print(f"[MODEL] Received batch size: {len(data)}")

        accuracy = evaluate_model(model, data)
        result = {'accuracy': accuracy}

        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_ML_UPLOADER_QUEUE,
            body=json.dumps(result)
        )
        print(f"[MODEL] Model's accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    start_model()
