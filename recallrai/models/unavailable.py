"""
Unavailable sentinel type for trusted reference objects.

When validation is skipped, some fields are intentionally unknown until the
resource is refreshed from the API. Use UNAVAILABLE to represent those fields.
"""

from typing import Literal, TypeAlias

Unavailable: TypeAlias = Literal["Unavailable"]
UNAVAILABLE: Unavailable = "Unavailable"
