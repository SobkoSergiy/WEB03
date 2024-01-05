# from datetime import datetime
import faker
from random import randint
import sqlite3


TOTAL_GROUPS = 3
TOTAL_STUDENTS = 30
TOTAL_TEACHERS = 4
TOTAL_SUBJECTS = 5
TOTAL_ASSESSMENTS = 4

def cram_groups(count):
    g = []
    # print("\ngroups tuples: (gr_id, gr_name)")
    for i in range(count):
        g.append((i+1, f"Group{i+1}"))
        # print(g[i])
    return g

def cram_students(count):
    s = []
    # print("\nstudents tuples: (st_name, st_group)")
    fr = faker.Faker() #("uk_UA")
    for i in range(count):
        g = i%TOTAL_GROUPS + 1
        s.append((fr.name()+f"({i+1}) (g{g})", g))
        # print(s[i])
    return s

def cram_teachers(count):
    t = []
    # print("\nteachers tuples: (tc_id, tc_name)")
    fr = faker.Faker()  #("uk_UA")
    for i in range(count):
        t.append((i+1, fr.name() + f"({i+1})"))
        # print(t[i])
    return t

def cram_subjects(count):
    s = []
    # print("\nsubjects tuples: (sj_name, sj_teach)")
    for i in range(count):
        t = i%TOTAL_TEACHERS + 1
        s.append((f"Subject{i+1} (t{t})", t))
        # print(s[i])
    return s

def cram_assessments(count): # French system: 0..20 points for academic performance
    a = []
    # print("\nassessments tuples: (as_assess, as_week, as_stud, as_subj)")
    for i in range(count):  
        # print(f"assessment week#{i+1}")
        for s in range(TOTAL_STUDENTS):
            # print("s=", s+1)
            for j in range(TOTAL_SUBJECTS):
                a.append((randint(1, 20),  i+1, s+1 , j+1))
                # print(a[-1])
    return a


def cram_tables():
    groups = cram_groups(TOTAL_GROUPS)
    students = cram_students(TOTAL_STUDENTS)
    teachers = cram_teachers(TOTAL_TEACHERS)
    subjects = cram_subjects(TOTAL_SUBJECTS)
    assessments = cram_assessments(TOTAL_ASSESSMENTS)

    with sqlite3.connect('modul06.db') as con:
        cur = con.cursor()

        sql_groups = """INSERT INTO groups(gr_id, gr_name) VALUES (?, ?)"""
        cur.executemany(sql_groups, groups)

        sql_students = """INSERT INTO students(st_name, st_group) VALUES (?, ?)"""
        cur.executemany(sql_students, students)

        sql_teachers = """INSERT INTO teachers(tc_id, tc_name) VALUES (?, ?)"""
        cur.executemany(sql_teachers, teachers)

        sql_subjects = """INSERT INTO subjects(sj_name, sj_teach) VALUES (?, ?)"""
        cur.executemany(sql_subjects, subjects)

        sql_assessments = """INSERT INTO assessments(as_assess, as_week, as_stud, as_subj)
                              VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_assessments, assessments)

        con.commit()    


def execute_query(sql: str) -> list:
    with sqlite3.connect('modul06.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()
    
    
def show_tables(table):
    clipp = execute_query(f"SELECT * FROM {table};")
    print(f">> Table {table}: total {len(clipp)} rows")
    for c in clipp:
        print(c)
    print()


def main():
    cram_tables()
    show_tables("groups")
    show_tables("students")
    show_tables("teachers")
    show_tables("subjects")
    show_tables("assessments")


if __name__ == "__main__":
    main()

