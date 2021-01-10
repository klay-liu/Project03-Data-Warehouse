import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Delete the pre-existing tables to ensure that our database does not throw any error if we try creating a table that already exists.

    Parameters:
           cur: a cursor returned by conn.cursor() used to interact with the database.
           conn: a connection object for database session with psycopg2.connect() method.

    Returns:
          None
   """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create tables that do not exist in database.

    Parameters:
        cur: a cursor returned by conn.cursor() used to interact with the database.
        conn: a connection object for database session with psycopg2.connect() method.

    Returns:
        None
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()