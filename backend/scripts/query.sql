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

-- Reporting Lines
select 
    farmers.id as farmer_id, 
    farmers.full_name as farmers_name, 
    count(field_jobs.id) as active_job_count
from farmers
join farms on farms.id = farmers.farm_id
join field_jobs on field_jobs.farmer_id = farmers.id
where 
    farms.supervisor_id = 1
    and field_jobs.status in ('Pending', 'In-Progress')
group by 
    farmers.id, 
    farmers.full_name
order by 
    farmers.id;
