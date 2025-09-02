import psycopg2
import connection
import logging


def delete_data(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student")
    cursor.execute("DELETE FROM room")
    conn.commit()


def create_indexes(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_room_id ON students(room_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_birthday ON students(birthday);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_sex ON students(sex);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_room_name ON rooms(name);")
    conn.commit()


def room_student_count(conn):

    try:
        with conn.cursor() as cur:
            cur.execute("""
                          SELECT rooms.id, rooms.name, COUNT(s.id) as student_count 
                          FROM students s
                          JOIN rooms ON s.room_id = rooms.id
                          GROUP BY rooms.id
                          ORDER BY student_count DESC;
                      """)
            results = cur.fetchall()
            return results

    except (Exception, psycopg2.Error) as error:
        logging.error(f"Ошибка при работе с PostgreSQL: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            logging.warning("\nСоединение с PostgreSQL закрыто.")


def rooms_with_youngest_students(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                            SELECT rooms.id, rooms.name, AVG(EXTRACT(YEAR FROM AGE(s.birthday))) as avg_age
                            FROM students s
                            JOIN rooms ON s.room_id = rooms.id
                            GROUP BY rooms.id
                            ORDER BY avg_age 
                            LIMIT 5;

                          """)
            results = cur.fetchall()
            return results

    except (Exception, psycopg2.Error) as error:
        logging.error(f"Ошибка при работе с PostgreSQL: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            logging.warning("\nСоединение с PostgreSQL закрыто.")


def rooms_with_max_age_gap(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                          SELECT rooms.id, rooms.name, MAX(EXTRACT(YEAR FROM AGE(s.birthday))) - MIN(EXTRACT(YEAR FROM AGE(s.birthday))) as age_gap
                            FROM students s
                            JOIN rooms ON s.room_id = rooms.id
                            GROUP BY rooms.id
                            ORDER BY age_gap DESC
                            LIMIT 5;

                      """)
            results = cur.fetchall()
            return results

    except (Exception, psycopg2.Error) as error:
        logging.error(f"Ошибка при работе с PostgreSQL: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            logging.warning("\nСоединение с PostgreSQL закрыто.")


def rooms_with_multiple_genders(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                          SELECT r.id, r.name
                          FROM rooms r
                          JOIN students s on s.room_id = r.id
                          GROUP BY r.id, r.name
                          HAVING COUNT(DISTINCT s.sex) > 1;

                      """)
            results = cur.fetchall()
            return results

    except (Exception, psycopg2.Error) as error:
        logging.error(f"Ошибка при работе с PostgreSQL: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            logging.warning("\nСоединение с PostgreSQL закрыто.")

