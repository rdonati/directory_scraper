import sqlite3
from sqlite3 import Error 
 
def selectAll(conn):
    sql = """
    SELECT * FROM students;
    """
    cur = conn.cursor()
    cur.execute(sql)
    students = cur.fetchall()
    print('Total # of students: ' + str(len(students)) + '\n')
    for student in students:
        s = ''
        s += ('ID: ' + str(student[0]) + '\n')
        s += ('First name: ' + student[1] + '\n')
        s += ('Second name: ' + str(student[2]) + '\n')
        s += ('Last name: ' + student[3] + '\n')
        s += ('Year: ' + str(student[4]) + '\n')
        s += ('Email: ' + student[5] + "\n\n")
        print(s)

def insertStudent(conn, firstName, secondName, lastName, classYear, email):

    sql = """
    INSERT INTO students(firstName, secondName, lastName, classYear, email)
    VALUES("%s", "%s", "%s", %s, "%s");
    """ % (firstName, secondName, lastName, classYear, email)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def clearTable(conn):
    sql = """
        DELETE FROM students;
        """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Table \"students\" has been cleared")

def createProject(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY,
            firstName TEXT NOT NULL,
            secondName TEXT,
            lastName TEXT NOT NULL,
            classYear INTEGER NOT NULL,
            email TEXT NOT NULL
        );
        """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected Successfuly")
    except Error as e:
        print(e)
    return conn