"""Feature Monitoring types."""
from .common import ExtendedEnum


class MonitorType(ExtendedEnum):
    """Type of monitoring data"""

    NUMERIC = "numeric"
    CATEGORY = "category"


class MonitorSourceType(ExtendedEnum):
    """Source of monitored variable source"""

    INPUT = "input"
    OUTPUT = "output"
    CUSTOM = "custom"
