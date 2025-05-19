import os
import pika
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()


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
    columns = list(data[0].keys())
    values = [[record.get(col) for col in columns] for record in data]

    cols_sql = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))

    sql = f"""
           INSERT INTO {table_name} ({cols_sql})
           VALUES ({placeholders})
           ON CONFLICT DO NOTHING;
       """

    try:
        cursor.executemany(sql, values)
        conn.commit()
        print(f"[INFO] Inserted {len(values)} records into {table_name}")
    except Exception as e:
        print(f"[ERROR] Batch insert into {table_name}: {e}")
        conn.rollback()


def raw_callback(ch, method, properties, body):
    match = json.loads(body)
    save_to_table(match, "raw_data")
    print(f"[RAW] Saved match {match.get('matchId')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def processed_callback(ch, method, properties, body):
    match = json.loads(body)
    save_to_table(match, "processed_data")
    print(f"[PROCESSED] Saved match {match.get('matchId')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


try:
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(queue='raw_data')
    channel.queue_declare(queue='processed_data')

    channel.basic_consume(queue='raw_data', on_message_callback=raw_callback)
    channel.basic_consume(queue='processed_data', on_message_callback=processed_callback)

    print("Uploader listening to 'raw_data' and 'processed_data' queues...")
    channel.start_consuming()
except KeyboardInterrupt:
    print("Shutting down uploader...")
    connection.close()
    conn.close()

