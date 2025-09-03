import psycopg2
import json
import os
from dotenv import load_dotenv
import connection
import logging
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


def load_data(conn, students_path, rooms_path):
    conn = None
    try:
        conn = connection.connection()

        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS students;")
            cur.execute("DROP TABLE IF EXISTS rooms CASCADE;")

            cur.execute("""
                CREATE TABLE rooms (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE students (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    birthday TIMESTAMP,
                    sex CHAR(1),
                    room_id INT,
                    CONSTRAINT fk_room
                        FOREIGN KEY(room_id) 
                        REFERENCES rooms(id)
                );
            """)

            with open(rooms_path, 'r', encoding='utf-8') as f:
                rooms_data = json.load(f)

            rooms_to_insert = [(room['id'], room['name']) for room in rooms_data]
            cur.executemany("INSERT INTO rooms (id, name) VALUES (%s, %s)", rooms_to_insert)

            with open(students_path, 'r', encoding='utf-8') as f:
                students_data = json.load(f)

            students_to_insert = [
                (student['id'], student['name'], student['birthday'], student['sex'], student['room'])
                for student in students_data
            ]

            cur.executemany(
                "INSERT INTO students (id, name, birthday, sex, room_id) VALUES (%s, %s, %s, %s, %s)",
                students_to_insert
            )

            conn.commit()

    except FileNotFoundError as e:
        logging.error(f"Ошибка: Файл не найден - {e}. Убедитесь, что файлы .json находятся в той же директории.")
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Ошибка при работе с PostgreSQL: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            logging.warning("\nСоединение с PostgreSQL закрыто.")


if __name__ == "__main__":
    load_data()
