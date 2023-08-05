"""
Enums related to deployment-api tests
"""
from taktile_types.enums.common import ExtendedEnum


class TestOutcomeColor(ExtendedEnum):
    """TestOutcomeColor.
    Color coded test outcome
    """

    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"


class TestTypes(ExtendedEnum):
    """TestTypes.
    Type of test
    """

    INTEGRATION = "integration"
    UNIT = "unit"
