SELECT g.gr_name, s.sj_name, a.as_assess, MAX(a.as_week)
FROM students st, subjects s, groups g 
JOIN assessments a ON (a.as_stud = st.st_id) AND (a.as_subj = s.sj_id) AND (st.st_group = g.gr_id)
GROUP BY st.st_id, s.sj_id
ORDER BY g.gr_name, s.sj_id
;