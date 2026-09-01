-- Reliability Metrics Query
SELECT equ.id AS equipment_id, CONCAT(SUM(CASE WHEN job.status = 'Completed' THEN 1 ELSE 0 END), ':',
	SUM(CASE WHEN job.status = 'Failed' THEN 1 ELSE 0 END)) AS completed_failed_ratio,
	equ.model
FROM equipments equ 
INNER JOIN field_jobs job ON job.equipment_id = equ.id
GROUP BY equ.model, equ.id;

-- Maintenance Flags Query
SELECT  f.id, f.name,
	CAST(SUM(CASE WHEN equ.status = 'Maintenance' THEN 1 ELSE 0 END) AS real)/COUNT(equ.id)
FROM farms f
INNER JOIN equipments equ ON f.id = equ.farm_id
GROUP BY f.name, f.id
HAVING CAST(SUM(CASE WHEN equ.status = 'Maintenance' THEN 1 ELSE 0 END) AS real)/COUNT(equ.id) > 0.3;
