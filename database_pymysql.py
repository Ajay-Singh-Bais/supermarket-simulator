import pymysql
from pymysql import MySQLError

def get_connection():
    try:
        conn = pymysql.connect(
            host='localhost', user='root', password='Tiger27&',
            database='supermarket', cursorclass= pymysql.cursors.DictCursor
        )
        return conn
    except MySQLError as e:
        print(f"Error occured while connecting to MySQL database: {e}")
        return None

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("SUCCESS: Successfully connected to MySQL database using pymysql.")
        conn.close()