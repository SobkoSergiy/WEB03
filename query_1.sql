SELECT st.st_name, ROUND(AVG(a.as_assess), 3) ra
FROM assessments a
LEFT JOIN students st ON a.as_stud = st.st_id
GROUP BY st.st_name
ORDER BY ra DESC
LIMIT 5
;