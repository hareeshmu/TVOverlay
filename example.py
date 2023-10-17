"""Example scripts for sending notifications."""
import asyncio

from tvoverlay import ConnectError, Notifications, Positions, Shapes

# from typing import Any


HOST = "10.10.10.111"


async def main() -> None:
    """Run the example script."""
    notifier = Notifications(HOST)

    # validate connection
    try:
        await notifier.async_connect()
    except ConnectError:
        return

    # Send a basic notification with message only
    await notifier.async_send("This is a notification message")

    # Customize all paramters in the notification
    response = await notifier.async_send(
        message="This is a notification message",
        title="Notification Title",
        id="0",
        appTitle="PyTest",
        appIcon="mdi:unicorn",
        color="#FFC107",
        image="https://picsum.photos/200/100",
        smallIcon="mdi:bell",
        largeIcon="mdi:home-assistant",
        corner=Positions.BOTTOM_LEFT,
        seconds=10,
    )

    print(response)

    response = await notifier.async_send_fixed(
        message="This is a notification message",
        id="0",
        icon="mdi:bell",
        textColor="#FFFFFF",
        iconColor="#FFFFFF",
        borderColor="#FFFFFF",
        backgroundColor="#000000",
        shape=Shapes.CIRCLE,
        expiration="120s",
        visible=True,
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
