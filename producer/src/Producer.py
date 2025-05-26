import pika
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

INPUT_CSV = os.getenv('INPUT_CSV', '/data/updated_match_data.csv')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbit-server')
RABBITMQ_PRODUCER_UPLOADER_QUEUE = os.getenv('RABBITMQ_PRODUCER_UPLOADER_QUEUE', 'producer_uploader_raw_data')
RABBITMQ_PRODUCER_PROCESSOR_QUEUE = os.getenv('RABBITMQ_PRODUCER_PROCESSOR_QUEUE', 'producer_processor_raw_data')


def main():
    try:
        df = pd.read_csv(INPUT_CSV)
        records = df.to_dict(orient="records")

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_PRODUCER_UPLOADER_QUEUE)
        channel.queue_declare(queue=RABBITMQ_PRODUCER_PROCESSOR_QUEUE)

        for i, record in enumerate(records):
            message = json.dumps(record)
            channel.basic_publish(exchange='',
                                  routing_key=RABBITMQ_PRODUCER_UPLOADER_QUEUE,
                                  body=message)
            channel.basic_publish(exchange='',
                                  routing_key=RABBITMQ_PRODUCER_PROCESSOR_QUEUE,
                                  body=message)
            print(f"[{i + 1}] Sent match record to queue {RABBITMQ_PRODUCER_UPLOADER_QUEUE}.")
            print(f"[{i + 1}] Sent match record to queue {RABBITMQ_PRODUCER_PROCESSOR_QUEUE}.")
       # time.sleep(SEND_DELAY)

        print("All data sent.")

    except Exception as e:
        print(f"Exception: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
