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