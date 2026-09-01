from enum import Enum

class EquipmentStatus(str, Enum):
    IDLE = "Idle"
    IN_MISSION = "In-Mission"
    MAINTENANCE = "Maintenance"
    OFFLINE = "Offline"

class FieldJobPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    CRITICAL = "Critical"

class FieldJobStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In-Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"

class UserRole(str, Enum):
    FARM_OPERATORS_ADMIN = "Farm Operations Admin"
    FIELD_HAND = "Field Hand"
    AUDITOR = "Auditor"
