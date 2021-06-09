import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


load_dotenv()
db_url = os.getenv('DB_URL')
table_name = "training"


def initialize_db():
    query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY NOT NULL,
        tweets TEXT NOT NULL,
        labels INT NOT NULL);"""
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(query)
    conn.commit()
    curs.close()
    conn.close()


def insert_data(tweet: str, label: int):
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    query = f"""
    INSERT INTO {table_name} 
    (tweets, labels)
    VALUES ('{tweet}',{label});"""
    curs.execute(query)
    conn.commit()
    curs.close()
    conn.close()


def load_data() -> list:
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    query = f"SELECT * FROM {table_name};"
    curs.execute(query)
    results = curs.fetchall()
    curs.close()
    conn.close()
    return results


def reset_table():
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    query = f"TRUNCATE TABLE {table_name} RESTART IDENTITY;"
    curs.execute(query)
    conn.commit()
    curs.close()
    conn.close()


def get_last_id() -> int:
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    query = f"SELECT MAX(id) FROM {table_name};"
    curs.execute(query)
    results = curs.fetchone()[0]
    curs.close()
    conn.close()
    return results or 0


def delete_by_id(idx):
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE id = {idx};"
    curs.execute(query)
    conn.commit()
    curs.close()
    conn.close()


if __name__ == '__main__':
    print("Index, Tweet, Rank")
    for row in load_data():
        print(', '.join(map(str, row)))
