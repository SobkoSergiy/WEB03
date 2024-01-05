SELECT t.tc_name, ROUND(AVG(a.as_assess), 2) ra
FROM assessments a
LEFT JOIN subjects s ON a.as_subj = s.sj_id
LEFT JOIN teachers t ON s.sj_teach = t.tc_id
GROUP BY t.tc_name
ORDER BY t.tc_id
;