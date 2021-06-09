import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


load_dotenv()
db_url = os.getenv('DB_URL')
table_name = "training"


def db_action(sql_action: str):
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(sql_action)
    conn.commit()
    curs.close()
    conn.close()


def db_query(sql_query) -> list:
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(sql_query)
    results = curs.fetchall()
    curs.close()
    conn.close()
    return results


def initialize_db():
    db_action(f"""CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY NOT NULL,
    tweets TEXT NOT NULL,
    labels INT NOT NULL);""")


def insert_data(tweet: str, label: int):
    db_action(f"""INSERT INTO {table_name} 
    (tweets, labels) 
    VALUES ('{tweet}',{label});""")


def load_data() -> list:
    return db_query(f"SELECT * FROM {table_name};")


def load_by_id(idx: int) -> list:
    return db_query(f"SELECT * FROM {table_name} WHERE id = {idx};")


def reset_table():
    db_action(f"TRUNCATE TABLE {table_name} RESTART IDENTITY;")


def delete_by_id(idx: int):
    db_action(f"DELETE FROM {table_name} WHERE id = {idx};")


if __name__ == '__main__':
    print("Index, Tweet, Rank")
    for row in load_data():
        print(', '.join(map(str, row)))
