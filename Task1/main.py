import queries
import connection
import load_data
import export_data
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_DEFAULT_PATH = os.path.join(BASE_DIR, 'jsons', 'students.json')
ROOMS_DEFAULT_PATH = os.path.join(BASE_DIR, 'jsons', 'rooms.json')


def main(students_path=STUDENTS_DEFAULT_PATH, rooms_path=ROOMS_DEFAULT_PATH):
    conn = connection.connection()
    load_data.load_data(conn, students_path, rooms_path)
    queries.create_indexes(conn)
    result = []

    result = queries.room_student_count(conn)
    # result += queries.rooms_with_youngest_students(conn)
    # result = queries.rooms_with_max_age_gap(conn)
    # result = queries.rooms_with_multiple_genders(conn)

    export_data.dump_json(result, "output")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        students_path = sys.argv[1]
        rooms_path = sys.argv[2]
        main(students_path, rooms_path)
    else:
        main()
