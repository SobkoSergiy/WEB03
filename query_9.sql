SELECT st.st_name, s.sj_name
FROM students st, subjects s, assessments a
WHERE (a.as_stud = st.st_id) AND (a.as_subj = s.sj_id) AND (a.as_week = 1)
ORDER BY st.st_id, s.sj_name
;