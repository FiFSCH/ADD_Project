from fastapi import FastAPI
from database import get_db_connection

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API WORKING 🗿🗿🗿🗿🗿"}


@app.get("/raw_data")
def get_raw_data(limit: int = 100):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM raw_data LIMIT {limit}")
    records = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, record)) for record in records]
    cursor.close()
    connection.close()
    return data
