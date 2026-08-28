-- Reliability Metrics Query
SELECT  SUM(CASE WHEN job.status = 'Completed' THEN 1 ELSE 0 END) AS completion_count,
	SUM(CASE WHEN job.status = 'Failed' THEN 1 ELSE 0 END) AS failed_count,
	equ.model
FROM equipments equ 
INNER JOIN field_jobs job ON job.equipment_id = equ.id
GROUP BY equ.model;

-- Maintenance Flags Query
SELECT  f.name,
	CAST(SUM(CASE WHEN equ.status = 'Maintenance' THEN 1 ELSE 0 END) AS real)/COUNT(equ.id)
FROM farms f
INNER JOIN equipments equ ON f.id = equ.farm_id
GROUP BY f.name
HAVING CAST(SUM(CASE WHEN equ.status = 'Maintenance' THEN 1 ELSE 0 END) AS real)/COUNT(equ.id) > 0.3;
