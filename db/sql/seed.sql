-- 1. Insert Farms
-- INSERT INTO farms (name, location_region, capacity, supervisor_id) VALUES
-- ('Jolly Ol'' Ranch', 'Kansas', 10, 1),
-- ('Farmhouse', 'Nevada', 50, 2);

-- 2. Insert Equipment
INSERT INTO equipments (serial_number, model, status, fuel_level, farm_id) VALUES
('HACH1', 'Hachet', 'Idle', 100.0, 1),
('HOE1', 'Hoe', 'Maintenance', 56.0, 1),
('BRM', 'Broom', 'In-Mission', 76.6, 2),
('SHOV1', 'Shovel', 'In-Mission', 40.2, 2),
('R1', 'Rake', 'In-Mission', 25.2, 2);

-- 3. Insert Farmers
-- INSERT INTO farmers (full_name, farm_id) VALUES
-- ('Billy Bob Jankins', 1),
-- ('Tom Sawyer', 1),
-- ('Lennie', 2),
-- ('George', 2),
-- ('Curley''s Wife', 2),
-- ('Slim', 2);

-- 4. Insert FieldJobs
INSERT INTO field_jobs (title, priority, status, equipment_id, farmer_id) VALUES
('Barn sweeping', 'Low', 'Pending', 3, 3),
('Grave Digging', 'Critical', 'In-Progress', 4, 4),
('Field Raking', 'Medium', 'Completed', 5, 1);

-- 5. Insert ServiceReports
INSERT INTO service_reports (file_url, notes, field_job_id) VALUES
('dumy', 'Lennie still hasn''t swept the barn?', 1),
('dumy', 'Hey! Who raked the fields? (Ooooo... spooky)', 3);

SELECT setval('farms_id_seq', (SELECT MAX(id) FROM farms));
SELECT setval('equipments_id_seq', (SELECT MAX(id) FROM equipments));
SELECT setval('farmers_id_seq', (SELECT MAX(id) FROM farmers));
SELECT setval('field_jobs_id_seq', (SELECT MAX(id) FROM field_jobs));
SELECT setval('service_reports_id_seq', (SELECT MAX(id) FROM service_reports));

COMMIT;
-- 6. Insert Users
-- Note: Replace the clear-text/mock functions with actual hashes if using psql directly
-- INSERT INTO "user" (username, hashed_password, role) VALUES
-- ('admin', 'password_hash_here', 'FARM_OPERATORS_ADMIN'),
-- ('farmer', 'password_hash_here', 'FIELD_HAND'),
-- ('auditor', 'password_hash_here', 'AUDITOR');
--
/*
--Robopulse Command Center - Day 2 Seed Data
-- Reusing the same data from day 1 so today's SQL results can be compared directly with
-- the script results from our vanilla python
-- psql -U postgres -d robopulse_dev_2478
-- \i seed.sql

--facilities records
INSERT INTO facilities (id, name, location_region, capacity, supervisor_id) VALUES
    (1, 'Houston Fabrication Plant', 'US-South', 40, 101),
    (2, 'Rotterdam Logistics Hub', 'EU-West', 25, 102);

--operators records
INSERT INTO operators (id, name, facility_id) VALUES
    (201, 'J. Alvarez', 1),
    (202, 'M. Chen', 1);

--robots records
INSERT INTO robots (id, serial_number, model, status, battery_level, facility_id) VALUES
    (1, 'RX-1001', 'Sentinel-V2', 'In-Mission', 18.5, 1),
    (2, 'RX-1002', 'Sentinel-V2', 'Idle', 76.0, 1),
    (3, 'AD-2050', 'SkyHawk-Drone', 'In-Mission', 9.0, 2),
    (4, 'RX-1003', 'Sentinel-V2', 'Maintenance', 42.0, 1);

--missions records
INSERT INTO missions (id, title, priority, status, robot_id, operator_id) VALUES
    (1, 'Pipeline Corrosion Sweep', 'Critical', 'Pending', 1, 201),
    (2, 'Warehouse Perimeter Patrol', 'Low', 'Pending', 3, 202),
    (3, 'Cooling Tower Inspection', 'Medium', 'Completed', 2, 201),
    (4, 'Fence Line Survey', 'Low', 'Failed', 4, 201);

--diagnostic log records
INSERT INTO diagnostic_logs (mission_id, file_url, notes) VALUES
    (1, 's3://robopulse-diagnostics/rx1001-001.pdf', 'Vibration sensor reading nominal');


--SELECT STATEMENTS AKA Queries
SELECT setval('facilities_id_seq', (SELECT MAX(id) FROM facilities));
SELECT setval('operators_id_seq', (SELECT MAX(id) FROM operators));
SELECT setval('robots_id_seq', (SELECT MAX(id) FROM robots));
SELECT setval('missions_id_seq', (SELECT MAX(id) FROM missions));
        Farm(name="Jolly Ol' Ranch", location_region="Kansas", capacity=10, supervisor_id=1),
        Farm(name="Farmhouse", location_region="Nevada", capacity=50, supervisor_id=2)

        Equipment(serial_number="HACH1", model="Hachet", status=EquipmentStatus.IDLE, fuel_level=100, farm_id=1),
        Equipment(serial_number="HOE1", model="Hoe", status=EquipmentStatus.MAINTENANCE, fuel_level=56.0, farm_id=1),
        Equipment(serial_number="BRM", model="Broom", status=EquipmentStatus.IN_MISSION, fuel_level=76.6, farm_id=2),
        Equipment(serial_number="SHOV1", model="Shovel", status=EquipmentStatus.IN_MISSION, fuel_level=40.2, farm_id=2),
        Equipment(serial_number="R1", model="Rake", status=EquipmentStatus.IN_MISSION, fuel_level=25.2, farm_id=2)

        Farmer(full_name="Billy Bob Jankins", farm_id=1),
        Farmer(full_name="Tom Sawyer", farm_id=1),
        Farmer(full_name="Lennie", farm_id=2),
        Farmer(full_name="George", farm_id=2),
        Farmer(full_name="Curley's Wife", farm_id=2),
        Farmer(full_name="Slim", farm_id=2)

        FieldJob(title="Barn sweeping",priority=FieldJobPriority.LOW,status=FieldJobStatus.PENDING,equipment_id=3,farmer_id=3),
        FieldJob(title="Grave Digging",priority=FieldJobPriority.CRITICAL,status=FieldJobStatus.IN_PROGRESS,equipment_id=4,farmer_id=4),
        FieldJob(title="Field Raking",priority=FieldJobPriority.MEDIUM,status=FieldJobStatus.COMPLETED,equipment_id=5,farmer_id=1)

        ServiceReport(file_url="dumy", notes="Lennie still hasn't swept the barn", field_job_id=1),
        ServiceReport(file_url="dumy", notes="Hey! Who raked the fields? (Ooooo... spooky)", field_job_id=3)

        User(username="admin", hashed_password=hash_password("password"), role=UserRole.FARM_OPERATORS_ADMIN),
        User(username="farmer", hashed_password=hash_password("password"), role=UserRole.FIELD_HAND),
        User(username="auditor", hashed_password=hash_password("password"), role=UserRole.AUDITOR)
*/
