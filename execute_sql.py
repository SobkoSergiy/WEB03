import sqlite3
from pathlib import Path


def read_sql(filename):
    p = Path(filename)
    sql = p.read_text()
    return sql

query_1 = '''--1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT st.st_name, ROUND(AVG(a.as_assess), 3) ra
FROM assessments a
LEFT JOIN students st ON a.as_stud = st.st_id
GROUP BY st.st_name
ORDER BY ra DESC
LIMIT 5
;
'''
query_2 = '''--2.Знайти студента із найвищим середнім балом з певного предмета.
SELECT temp.st_name, temp.sj_name, MAX(temp.ra) mtra, temp.sa 
FROM (
	SELECT st.st_name, s.sj_id, s.sj_name, AVG(a.as_assess) ra, SUM(a.as_assess) sa
	FROM assessments a, subjects s, students st 
	WHERE (a.as_subj = s.sj_id) AND (a.as_stud = st.st_id)
	GROUP BY st.st_id, s.sj_id
	) temp
GROUP BY temp.sj_id 
ORDER BY temp.sj_id	
;
'''
query_3 = '''--3.Знайти середній бал у групах з певного предмета.
SELECT g.gr_name, s.sj_name, ROUND(AVG(a.as_assess), 3)
FROM assessments a
LEFT JOIN subjects s ON a.as_subj = s.sj_id
LEFT JOIN students st ON a.as_stud = st.st_id
LEFT JOIN groups g ON st.st_group = g.gr_id
GROUP BY s.sj_name, g.gr_name
ORDER BY g.gr_name
;
'''
query_4 = '''--4.Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT ROUND(AVG(a.as_assess), 2)
FROM assessments
;
'''
query_5 = '''--5.Знайти які курси читає певний викладач.
SELECT t.tc_name, s.sj_name 
FROM teachers t 
LEFT JOIN subjects s ON s.sj_teach = t.tc_id
ORDER BY t.tc_id 
;
'''
query_6 = '''--6.Знайти список студентів у певній групі.
SELECT g.gr_name, s.st_name  
FROM groups g, students s
WHERE s.st_group = g.gr_id
ORDER BY g.gr_id
;
'''
query_7 = '''--7.Знайти оцінки студентів у окремій групі з певного предмета.
SELECT g.gr_name, s.sj_name, a.as_assess
FROM assessments a
LEFT JOIN subjects s ON a.as_subj = s.sj_id
LEFT JOIN students st ON a.as_stud = st.st_id
LEFT JOIN groups g ON st.st_group = g.gr_id
ORDER BY g.gr_name, s.sj_name
;
'''
query_8 = '''--8.Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT t.tc_name, s.sj_name, ROUND(AVG(a.as_assess), 2) ra
FROM assessments a
LEFT JOIN subjects s ON a.as_subj = s.sj_id
LEFT JOIN teachers t ON s.sj_teach = t.tc_id
GROUP BY t.tc_name, s.sj_name
ORDER BY t.tc_id
;
'''
query_9 = '''--9.Знайти список курсів, які відвідує студент.
SELECT st.st_name, s.sj_name
FROM students st, subjects s, assessments a
WHERE (a.as_stud = st.st_id) AND (a.as_subj = s.sj_id) AND (a.as_week = 1)
ORDER BY st.st_id, s.sj_name
;
'''
query_10 = '''--10.Список курсів, які певному студенту читає певний викладач.
SELECT t.tc_name, st.st_name, s.sj_name
FROM students st, subjects s, teachers t, assessments a
WHERE (a.as_stud = st.st_id) AND (a.as_subj = s.sj_id) AND (s.sj_teach = t.tc_id ) AND (a.as_week = 1)
ORDER BY t.tc_id , st.st_id, s.sj_id
;
'''
query_11 = '''--11. Середній бал, який певний викладач ставить певному студентові.
SELECT t.tc_name, ROUND(AVG(a.as_assess), 2) ra
FROM assessments a
LEFT JOIN subjects s ON a.as_subj = s.sj_id
LEFT JOIN teachers t ON s.sj_teach = t.tc_id
GROUP BY t.tc_name
ORDER BY t.tc_id
;
'''
query_12 = '''--12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT g.gr_name, s.sj_name, a.as_assess, MAX(a.as_week)
FROM students st, subjects s, groups g 
JOIN assessments a ON (a.as_stud = st.st_id) AND (a.as_subj = s.sj_id) AND (st.st_group = g.gr_id)
GROUP BY st.st_id, s.sj_id
ORDER BY g.gr_name, s.sj_id
;
'''

tasks = [
"1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.",
"2.Знайти студента із найвищим середнім балом з певного предмета.",
"3.Знайти середній бал у групах з певного предмета.",
"4.Знайти середній бал на потоці (по всій таблиці оцінок).",
"5.Знайти які курси читає певний викладач.",
"6.Знайти список студентів у певній групі.",
"7.Знайти оцінки студентів у окремій групі з певного предмета.",
"8.Знайти середній бал, який ставить певний викладач зі своїх предметів.",
"9.Знайти список курсів, які відвідує студент.",
"10.Список курсів, які певному студенту читає певний викладач.",
"11. Середній бал, який певний викладач ставить певному студентові.",
"12. Оцінки студентів у певній групі з певного предмета на останньому занятті."
]

def execute_query(database, task, hdisk=True ):
    t = task if 1 <= task <= 12 else 1
    sql = read_sql(f'query_{t}.sql') if hdisk  else globals()[f'query_{t}']      
    print(f">> query sql #{t}: {sql}")

    with sqlite3.connect(database) as con:
        cur = con.cursor()
        cur.execute(sql)     
        res = cur.fetchall()
        print(f">> query result: total {len(res)} rows")
        for r in res:
            print(r)
    print()


def main():
    task = 1  # 1..12
    data = 'modul06.db'  # 'tutorial.db'
    execute_query(data, task, hdisk=False)


if __name__ == "__main__":
    main()