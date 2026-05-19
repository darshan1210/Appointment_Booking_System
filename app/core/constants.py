"""Application constants."""
from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    FIRM_ADMIN = "firm_admin"
    USER = "user"


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    QUEUED = "queued"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"


class CampaignChannel(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    BOTH = "both"


class NotificationType(str, Enum):
    APPOINTMENT_REQUEST = "appointment_request"
    APPOINTMENT_ACCEPTED = "appointment_accepted"
    APPOINTMENT_DECLINED = "appointment_declined"
    APPOINTMENT_CANCELLED = "appointment_cancelled"
    REMINDER_10MIN = "reminder_10min"
    REMINDER_1MIN = "reminder_1min"
    CAMPAIGN = "campaign"
    SYSTEM = "system"


class FirmStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class FirmPlan(str, Enum):
    FREE = "free"
    BASIC = "basic"
    ENTERPRISE = "enterprise"
