import pika
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

INPUT_CSV = os.getenv('INPUT_CSV', '../data/updated_match_data.csv')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbit-server')
RABBITMQ_RAW_QUEUE = os.getenv('RABBITMQ_RAW_QUEUE', 'raw_data')
RABBITMQ_PROCESSED_QUEUE = os.getenv('RABBITMQ_PROCESSED_QUEUE', 'processed_data')
SEND_DELAY = float(os.getenv('SEND_DELAY', '0.01'))


def main():
    try:
        df = pd.read_csv(INPUT_CSV)
        records = df.to_dict(orient="records")

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_RAW_QUEUE)


# TODO POSSIBLE BATCH REFACTOR
        message = json.dumps(records)
        channel.basic_publish(exchange='',
                                  routing_key=RABBITMQ_RAW_QUEUE,
                                  body=message)
       # print(f"[{i + 1}] Sent match record to queue.")
       # time.sleep(SEND_DELAY)

        print("All data sent.")

    except Exception as e:
        print(f"Exception: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
