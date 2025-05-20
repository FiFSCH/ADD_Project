import os
import pika
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_PRODUCER_UPLOADER_QUEUE = os.getenv('RABBITMQ_PRODUCER_UPLOADER_QUEUE', 'producer_uploader_raw_data')
RABBITMQ_PROCESSOR_UPLOADER_QUEUE = os.getenv('RABBITMQ_PROCESSOR_UPLOADER_QUEUE', 'processor_uploader_processed_data')
RABBITMQ_ML_UPLOADER_QUEUE = os.getenv('RABBITMQ_ML_UPLOADER_QUEUE', 'ml_uploader_metrics_data')
RAW_DATA_TABLE = os.getenv('RAW_DATA_TABLE', 'raw_data')
PROCESSED_DATA_TABLE = os.getenv('PROCESSED_DATA_TABLE', 'processed_data')
METRICS_TABLE = os.getenv('METRICS_TABLE', 'ml_metrics')


def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'lol_data'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
        host=os.getenv('DB_HOST', 'database'),
        port=os.getenv('DB_PORT', '5432')
    )


def get_rabbitmq_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'rabbit-server'),
        port=int(os.getenv('RABBITMQ_PORT', '5672')),
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_USER', 'guest'),
            password=os.getenv('RABBITMQ_PASSWORD', 'guest')
        )))


conn = get_db_connection()
cursor = conn.cursor()


def save_to_table(data, table_name):
    columns = list(data.keys())
    values = [data[col] for col in columns]

    cols_sql = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))

    sql = f"""
           INSERT INTO {table_name} ({cols_sql})
           VALUES ({placeholders})
           ON CONFLICT DO NOTHING;
       """

    try:
        cursor.execute(sql, values)
        conn.commit()
        print(f"[INFO] Inserted {len(values)} records into {table_name}")
    except Exception as e:
        print(f"[ERROR] Inserting into {table_name}: {e}")
        conn.rollback()


def raw_callback(ch, method, properties, body):
    match = json.loads(body)
    save_to_table(match, RAW_DATA_TABLE)
    print(f"[{RAW_DATA_TABLE}] Saved match {match.get('matchId')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def processed_callback(ch, method, properties, body):
    match = json.loads(body)
    save_to_table(match, PROCESSED_DATA_TABLE)
    print(f"[{PROCESSED_DATA_TABLE}] Saved match {match.get('matchId')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def metrics_callback(ch, method, properties, body):
    match = json.loads(body)
    save_to_table(match, METRICS_TABLE)
    print(f"[{METRICS_TABLE}] Saved match {match.get('matchId')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


try:
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_PRODUCER_UPLOADER_QUEUE)
    channel.queue_declare(queue=RABBITMQ_PROCESSOR_UPLOADER_QUEUE)
    channel.queue_declare(queue=RABBITMQ_ML_UPLOADER_QUEUE)

    channel.basic_consume(queue=RABBITMQ_PRODUCER_UPLOADER_QUEUE, on_message_callback=raw_callback)
    channel.basic_consume(queue=RABBITMQ_PROCESSOR_UPLOADER_QUEUE, on_message_callback=processed_callback)
    channel.basic_consume(queue=RABBITMQ_ML_UPLOADER_QUEUE, on_message_callback=metrics_callback)

    print(f"Uploader listening to {RABBITMQ_PRODUCER_UPLOADER_QUEUE}, {RABBITMQ_PROCESSOR_UPLOADER_QUEUE}, {RABBITMQ_ML_UPLOADER_QUEUE} queues...")
    channel.start_consuming()
except KeyboardInterrupt:
    print("Shutting down uploader...")
    connection.close()
    conn.close()

