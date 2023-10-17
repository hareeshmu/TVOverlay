"""Library for sending notifications to TVOverlay."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from .const import (
    DEFAULT_APP_ICON,
    DEFAULT_APP_TITLE,
    DEFAULT_COLOR,
    DEFAULT_DURATION,
    DEFAULT_LARGE_ICON,
    DEFAULT_SMALL_ICON,
    DEFAULT_TITLE,
    Positions,
    Shapes,
)
from .exceptions import ConnectError, InvalidResponse

_LOGGER = logging.getLogger(__name__)


class ImageUrlSource:
    """Image source from url or local path."""

    def __init__(
        self,
        url: str,
        username: str | None = None,
        password: str | None = None,
        auth: str | None = None,
    ) -> None:
        """Initiate image source class."""
        self.url = url
        self.auth: httpx.BasicAuth | httpx.DigestAuth | None = None

        if auth:
            if auth not in ["basic", "disgest"]:
                raise ValueError("authentication must be 'basic' or 'digest'")
            if username is None or password is None:
                raise ValueError("username and password must be specified")
            if auth == "basic":
                self.auth = httpx.BasicAuth(username, password)
            else:
                self.auth = httpx.DigestAuth(username, password)


class Notifications:
    """Notifications class for TVOverlay."""

    def __init__(
        self,
        host: str,
        port: int = 5001,
        httpx_client: httpx.AsyncClient | None = None,
    ) -> None:
        """Initialize notifier."""
        self.url = f"http://{host}:{port}"
        self.httpx_client = httpx_client

        self.DEFAULT_APP_ICON = DEFAULT_APP_ICON
        self.DEFAULT_APP_TITLE = DEFAULT_APP_TITLE
        self.DEFAULT_COLOR = DEFAULT_COLOR
        self.DEFAULT_LARGE_ICON = DEFAULT_LARGE_ICON
        self.DEFAULT_SMALL_ICON = DEFAULT_SMALL_ICON
        self.DEFAULT_TITLE = DEFAULT_TITLE
        self.DEFAULT_DURATION = DEFAULT_DURATION
        self.Positions = Positions
        self.Shapes = Shapes

    async def async_connect(self) -> None:
        """Test connecting to server."""
        httpx_client: httpx.AsyncClient = (
            self.httpx_client if self.httpx_client else httpx.AsyncClient(verify=False)
        )
        try:
            async with httpx_client as client:
                await client.get(self.url + "/get", timeout=5)
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(f"Connection to {self.url} failed") from err

    async def async_send(
        self,
        message: str,
        title: str = DEFAULT_TITLE,
        id: str | None = None,
        appTitle: str = DEFAULT_APP_TITLE,
        appIcon: str = DEFAULT_APP_ICON,
        color: str = DEFAULT_COLOR,
        image: str | None = None,
        smallIcon: str = DEFAULT_SMALL_ICON,
        largeIcon: str = DEFAULT_LARGE_ICON,
        corner: Positions = Positions.TOP_RIGHT,
        seconds: int = DEFAULT_DURATION,
    ) -> str:
        """Send notification with parameters.

        :param message: The notification message.
        :param title: (Optional) The notification title.
        :param id: (Optional) ID - Ff a notification is being displayed and the tvoverlay receives a notification with the same id, the notification displayed is updated instantly
        :param appTitle: (Optional) App Title text field.
        :param appIcon: (Optional) Accepts mdi icons, image urls and Bitmap encoded to Base64.
        :param color: (Optional) appIcon color accepts 6 or 8 digit color hex. the '#' is optional.
        :param image: (Optional) Accepts mdi icons, image urls.
        :param smallIcon: (Optional) Accepts mdi icons, image urls and Bitmap encoded to Base64.
        :param largeIcon: (Optional) Accepts mdi icons, image urls and Bitmap encoded to Base64.
        :param corner: (Optional) Notification Position values: bottom_start, bottom_end, top_start, top_end.
        :param seconds: (Optional) Display the notification for the specified period in seconds.

        Usage:
        >>> from tvoverlay import Notifications
        >>> notifier = Notifications("192.168.1.100")
        >>> notifier.async_send(
                "message to be sent",
                "title"="Notification title",
                "id": 0,
                "appTitle": "MyApp",
                "appIcon": "mdi:unicorn",
                "color": "#FF0000",
                "image": "https://picsum.photos/200/100",
                "smallIcon": "mdi:bell",
                "largeIcon": "mdi:home-assistant",
                "corner": "bottom_end",
                "seconds": 20
            )
        """
        data: dict[str, Any] = {
            "message": message,
            "title": title,
            "id": id,
            "appTitle": appTitle,
            "appIcon": appIcon,
            "color": color,
            "image": image,
            "smallIcon": smallIcon,
            "largeIcon": largeIcon,
            "corner": corner.value,
            "seconds": seconds,
        }

        headers = {"Content-Type": "application/json"}

        _LOGGER.debug("data: %s", data)

        print(data)

        httpx_client: httpx.AsyncClient = (
            self.httpx_client if self.httpx_client else httpx.AsyncClient(verify=False)
        )

        try:
            async with httpx_client as client:
                response = await client.post(
                    self.url + "/notify", json=data, headers=headers, timeout=5
                )
            # response.raise_for_status()
            # json_response = response.json()
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(
                f"Error sending notification to {self.url}: {err}"
            ) from err
        if response.status_code == httpx.codes.OK:
            return "Success"
        else:
            raise InvalidResponse(f"Error sending notification: {response}")

    async def async_send_fixed(
        self,
        message: str,
        id: str | None = None,
        icon: str = DEFAULT_APP_ICON,
        textColor: str = "#FFFFFF",
        iconColor: str = "#FFFFFF",
        borderColor: str = "#FFFFFF",
        backgroundColor: str = "#000000",
        shape: Shapes = Shapes.CIRCLE,
        expiration: str = "5s",
        visible: bool = True,
    ) -> str:
        """Send Fixed notification.

        :param message: "Sample" # REQUIRED: this is a required field for home assistant, but it can be 'null' if not needed
        :param id: "fixed_notification_sample" # optional id string - if a fixed notification with this id exist, it will be updated
        :param icon: mdi:unicorn  # optional - accepts mdi icons, image urls and Bitmap encoded to Base64
        :param textColor: "#FFF000" # optional - accepts 6 or 8 digit color hex. the '#' is optional
        :param iconColor: "#FFF000" # optional - accepts 6 or 8 digit color hex. the '#' is optional
        :param borderColor: "#FFF000" # optional - accepts 6 or 8 digit color hex. the '#' is optional
        :param backgroundColor: "#FFF000" # optional - accepts 6 or 8 digit color hex. the '#' is optional
        :param shape: "circle" # optional - values: circle, rounded, rectangular
        :param expiration: "7m"  # optional - valid formats: 1695693410 (Epoch time), 1y2w3d4h5m6s (duration format) or 123 (for seconds)
        :param visible: true  # optional - if false it deletes the fixed notification with matching id

        Usage:
        >>> from tvoverlay import Notifications
        >>> notifier = Notifications("192.168.1.100")
        >>> notifier.async_send_fixed(
                message: "Sample"
                id: "fixed_notification_sample"
                icon: "mdi:bell"
                textColor: "#FFF000"
                iconColor: "#FFF000"
                borderColor: "#FFF000"
                backgroundColor: "#FFF000"
                shape: "circle"
                expiration: "7m"
                visible: true
            )
        """
        data: dict[str, Any] = {
            "message": message,
            "id": id,
            "textColor": textColor,
            "icon": icon,
            "iconColor": iconColor,
            "borderColor": borderColor,
            "backgroundColor": backgroundColor,
            "shape": shape.value,
            "expiration": expiration,
            "visible": visible,
        }

        headers = {"Content-Type": "application/json"}

        _LOGGER.debug("data: %s", data)

        print(data)

        httpx_client: httpx.AsyncClient = (
            self.httpx_client if self.httpx_client else httpx.AsyncClient(verify=False)
        )

        try:
            async with httpx_client as client:
                response = await client.post(
                    self.url + "/notify_fixed", json=data, headers=headers, timeout=5
                )
            # response.raise_for_status()
            # json_response = response.json()
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(
                f"Error sending fixed notification to {self.url}: {err}"
            ) from err
        if response.status_code == httpx.codes.OK:
            return "Success"
        else:
            raise InvalidResponse(f"Error sending fixed notification: {response}")
