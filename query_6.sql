SELECT g.gr_name, s.st_name  
FROM groups g, students s
WHERE s.st_group = g.gr_id
ORDER BY g.gr_id
;