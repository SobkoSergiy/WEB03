SELECT t.tc_name, s.sj_name 
FROM teachers t 
LEFT JOIN subjects s ON s.sj_teach = t.tc_id
ORDER BY t.tc_id 
;