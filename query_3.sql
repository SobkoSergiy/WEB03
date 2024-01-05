SELECT g.gr_name, s.sj_name, ROUND(AVG(a.as_assess), 3)
FROM assessments a
LEFT JOIN subjects s ON a.as_subj = s.sj_id
LEFT JOIN students st ON a.as_stud = st.st_id
LEFT JOIN groups g ON st.st_group = g.gr_id
GROUP BY s.sj_name, g.gr_name
ORDER BY g.gr_name
;