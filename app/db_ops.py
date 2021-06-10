import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


load_dotenv()
db_url = os.getenv('DB_URL')
table_name = "training"


def db_action(sql_action: str):
    """ DB Setter - Performs a DB action returns None """
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(sql_action)
    conn.commit()
    curs.close()
    conn.close()


def db_query(sql_query) -> list:
    """ DB Getter - Returns query results as a list """
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()
    curs.execute(sql_query)
    results = curs.fetchall()
    curs.close()
    conn.close()
    return results


def initialize_db():
    """ Database table initialization - only required once """
    db_action(f"""CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY NOT NULL,
    tweets TEXT NOT NULL,
    labels INT NOT NULL);""")


def insert_data(tweet: str, label: int):
    """ Inserts a new row """
    db_action(f"""INSERT INTO {table_name} 
    (tweets, labels) 
    VALUES ('{tweet}',{label});""")


def load_data(n_rows) -> list:
    """ Returns the most recent n_rows in reverse chronological order """
    return db_query(f"""SELECT * FROM {table_name}
    ORDER BY id DESC LIMIT {n_rows};""")


def load_by_id(idx: int) -> list:
    """ Returns a row by the primary key: id """
    return db_query(f"SELECT * FROM {table_name} WHERE id = {idx};")


def reset_table():
    """ DANGER!!! This will remove ALL rows in the database """
    db_action(f"TRUNCATE TABLE {table_name} RESTART IDENTITY;")


def delete_by_id(idx: int):
    """ Deletes a row by the primary key: id """
    db_action(f"DELETE FROM {table_name} WHERE id = {idx};")


def update_rank_by_id(idx, rank):
    db_action(f"""UPDATE {table_name} 
    SET labels = {rank} 
    WHERE id = {idx};""")
