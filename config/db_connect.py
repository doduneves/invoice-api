
import psycopg2
from config import config


def connect_db():
    conn = None
    try:
        params = config.config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        cur = conn.cursor()
        
        return (conn, cur)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()