SELECT g.gr_name, s.sj_name, a.as_assess
FROM assessments a
LEFT JOIN subjects s ON a.as_subj = s.sj_id
LEFT JOIN students st ON a.as_stud = st.st_id
LEFT JOIN groups g ON st.st_group = g.gr_id
ORDER BY g.gr_name, s.sj_name
;