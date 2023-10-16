"""Constants for the library."""

from enum import Enum
from typing import Final

DEFAULT_TITLE: Final = "Notification"
DEFAULT_APP_TITLE: Final = "Notification"
DEFAULT_APP_ICON: Final = "mdi:bell"
DEFAULT_SMALL_ICON: Final = "mdi:bell"
DEFAULT_LARGE_ICON: Final = "mdi:home-assistant"
DEFAULT_COLOR: Final = "#049cdb"


class Positions(Enum):
    """Supported positions for the notification overlay."""

    BOTTOM_RIGHT = "bottom_end"
    BOTTOM_LEFT = "bottom_start"
    TOP_RIGHT = "top_end"
    TOP_LEFT = "top_start"


class Shapes(Enum):
    """Supported positions for the notification overlay."""

    CIRCLE = "circle"
    ROUNDED = "rounded"
    RECTANGULAR = "rectangular"

