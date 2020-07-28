
import psycopg2
from .config import config


def connect_db():
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        cur = conn.cursor()
        
        return (conn, cur)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None, None



def close_db(conn, cur):
    if cur is not None:
        cur.close()
    
    if conn is not None:
        conn.close()