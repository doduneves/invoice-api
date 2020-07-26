
import psycopg2
from config import config

def create_table():

    create_command = (
        """
        CREATE TABLE invoices (
            id uuid PRIMARY KEY,
            document VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            amount DECIMAL NOT NULL,
            referenceMonth DATE NOT NULL,
            referenceYear INTEGER NOT NULL,
            createdAt TIMESTAMP NOT NULL,
            isActive BOOLEAN NOT NULL,
            deactiveAt TIMESTAMP
        )
        """)
    conn = None
    try:

        params = config.config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print("Generating Invoices table")
        cur.execute(create_command)

        cur.close()

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_table()