import os
import json
import pika
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

OG_COLUMNS = [
    'matchId', 'blueTeamControlWardsPlaced', 'blueTeamWardsPlaced',
    'blueTeamTotalKills', 'blueTeamDragonKills', 'blueTeamHeraldKills',
    'blueTeamTowersDestroyed', 'blueTeamInhibitorsDestroyed',
    'blueTeamTurretPlatesDestroyed', 'blueTeamFirstBlood',
    'blueTeamMinionsKilled', 'blueTeamJungleMinions', 'blueTeamTotalGold',
    'blueTeamXp', 'blueTeamTotalDamageToChamps', 'redTeamControlWardsPlaced',
    'redTeamWardsPlaced', 'redTeamTotalKills', 'redTeamDragonKills',
    'redTeamHeraldKills', 'redTeamTowersDestroyed',
    'redTeamInhibitorsDestroyed', 'redTeamTurretPlatesDestroyed',
    'redTeamMinionsKilled', 'redTeamJungleMinions', 'redTeamTotalGold',
    'redTeamXp', 'redTeamTotalDamageToChamps', 'blueWin'
]

COLUMNS_TO_DROP = [
    'blueTeamControlWardsPlaced', 'blueTeamWardsPlaced', 'blueTeamInhibitorsDestroyed',
    'redTeamInhibitorsDestroyed', 'redTeamControlWardsPlaced', 'redTeamWardsPlaced'
]

def get_rabbitmq_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'rabbit-server'),
        port=int(os.getenv('RABBITMQ_PORT', '5672')),
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_USER', 'guest'),
            password=os.getenv('RABBITMQ_PASSWORD', 'guest')
        )))


def process_match(match):
    try:
        match_data = {key: match[key] for key in OG_COLUMNS if key in match}
        df = pd.DataFrame([match_data])

        df_processed = df.drop(columns=COLUMNS_TO_DROP)

        df_processed['gold_difference'] = df['blueTeamTotalGold'] - df['redTeamTotalGold']

        return df_processed.to_dict(orient='records')[0]
    except Exception as e:
        print(f"[ERROR] Processing match: {e}")
        return None


def callback(ch, method, properties, body):
    try:
        match = json.loads(body)
        processed = process_match(match)

        if processed:
            # Send to processed Q
            ch.basic_publish(
                exchange='',
                routing_key='processed_data',
                body=json.dumps(processed)
            )
            print(f"[PROCESSOR] Processed match: {processed['matchId']}")
        else:
            print("[PROCESSOR] Processing error")

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[PROCESSOR ERROR] {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def start_processor():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(queue='raw_data')
    channel.queue_declare(queue='processed_data')

    channel.basic_consume(queue='raw_data', on_message_callback=callback)

    print("[PROCESSOR] Listening...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("[PROCESSOR] Exiting...")
        channel.close()
        connection.close()


if __name__ == "__main__":
    start_processor()

# TODO add sending messages to ML component
