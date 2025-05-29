from fastapi import FastAPI, Query
from database import get_db_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "API WORKING 🗿🗿🗿🗿🗿"}


@app.get("/raw_data")
# def get_raw_data(limit: int = 100):
def get_raw_data(limit: int = Query(default=None, description="Optional row limit")):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM raw_data"
    if limit:
        query += f" LIMIT {limit}"
    cursor.execute(query)
    records = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, record)) for record in records]
    cursor.close()
    connection.close()
    return data


@app.get("/processed_data")
def get_processed_data(limit: int = Query(default=None, description="Optional row limit")):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM processed_data"
    if limit:
        query += f" LIMIT {limit}"
    cursor.execute(query)
    records = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, record)) for record in records]
    cursor.close()
    connection.close()
    return data


@app.get("/ml_metrics")
def get_ml_metrics(limit: int = Query(default=None, description="Optional row limit")):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM ml_metrics"
    if limit:
        query += f" LIMIT {limit}"
    cursor.execute(query)
    records = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, record)) for record in records]
    cursor.close()
    connection.close()
    return data

# @app.get("/ml_metrics")
# # def get_raw_data(limit: int = 100):
# def get_raw_data():
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT * FROM ml_metrics")
#     records = cursor.fetchall()
#     columns = [desc[0] for desc in cursor.description]
#     data = [dict(zip(columns, record)) for record in records]
#     cursor.close()
#     connection.close()
#     return data
