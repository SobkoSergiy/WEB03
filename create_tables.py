import sqlite3

sql_create_groups = '''
CREATE TABLE IF NOT EXISTS groups (
   gr_id INTEGER PRIMARY KEY,
   gr_name CHAR(10)
);
'''
sql_create_students = '''
CREATE TABLE IF NOT EXISTS students (
   st_id INTEGER PRIMARY KEY AUTOINCREMENT,
   st_name VARCHAR(30),
   st_group INTEGER, FOREIGN KEY (st_group) REFERENCES groups (gr_id)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
);
'''
sql_create_teachers = '''
CREATE TABLE IF NOT EXISTS teachers (
   tc_id INTEGER PRIMARY KEY,
   tc_name VARCHAR(30)
);
'''
sql_create_subjects = '''
CREATE TABLE IF NOT EXISTS subjects (
   sj_id INTEGER PRIMARY KEY AUTOINCREMENT,
   sj_name VARCHAR(25) UNIQUE NOT NULL,
   sj_teach INTEGER, FOREIGN KEY (sj_teach) REFERENCES teachers (tc_id)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT
);
'''
#DROP TABLE IF EXISTS assessments;
sql_create_assessments = '''
CREATE TABLE IF NOT EXISTS assessments (
   as_id INTEGER PRIMARY KEY AUTOINCREMENT,
   as_assess TINYINT UNSIGNED NOT NULL,
   as_number TINYINT UNSIGNED NOT NULL,
   as_subj INTEGER, 
   as_stud INTEGER, 
   FOREIGN KEY (as_subj) REFERENCES subjects (sj_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE   
   FOREIGN KEY (as_stud) REFERENCES students (st_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
'''

def create_tables():
    with sqlite3.connect('tutorial.db') as con:
        cur = con.cursor()
        cur.execute(sql_create_groups)
        cur.execute(sql_create_students)
        cur.execute(sql_create_teachers)
        cur.execute(sql_create_subjects)
        cur.execute(sql_create_assessments)
      #   cur.executescript(sql_create_assessments)

    print("Tables created")



def main():
    create_tables()

if __name__ == "__main__":
    main()