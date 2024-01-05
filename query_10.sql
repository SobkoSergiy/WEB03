SELECT t.tc_name, st.st_name, s.sj_name
FROM students st, subjects s, teachers t, assessments a
WHERE (a.as_stud = st.st_id) AND (a.as_subj = s.sj_id) AND (s.sj_teach = t.tc_id ) AND (a.as_week = 1)
ORDER BY t.tc_id , st.st_id, s.sj_id
;