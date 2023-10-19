"""Example scripts for sending notifications."""
import asyncio

from tvoverlay import ConnectError, Notifications


# from typing import Any


HOST = "10.10.10.113"

# HOST = "0.0.0.0"


async def main() -> None:
    """Run the example script."""
    notifier = Notifications(HOST)


    # print("Invalid position value. Has to be one of %s", [member.value for member in Positions])
    # Positions.TOP_RIGHT
    # corner = Positions.TOP_RIGHT
    # print(corner.value)

    # validate connection
    try:
        response = await notifier.async_connect()
        print(response)
    except ConnectError:
        print("Connect Error")

    print("======================")
    # Send a basic notification with message only
    print(await notifier.async_send("This is a notification message"))

    print("======================")

    # Customize all paramters in the notification
    # response = await notifier.async_send(
    #     message="This is a notification message",
    #     title="Notification Title",
    #     id="0",
    #     appTitle="PyTest",
    #     appIcon="mdi:unicorn",
    #     color="#FFC107",
    #     image="https://picsum.photos/200/100",
    #     smallIcon="mdi:bell",
    #     largeIcon="mdi:home-assistant",
    #     corner=Positions.BOTTOM_LEFT,
    #     seconds=10,
    # )

    # print(response)

    # response = await notifier.async_send(
    #     message="This is a notification message",
    #     title="Notification Title",
    #     id="0",
    #     appTitle="PyTest",
    #     appIcon="mdi:unicorn",
    #     smallIconColor="#FFC107",
    #     image=ImageUrlSource("https://picsum.photos/200/100"),
    #     smallIcon="mdi:bell",
    #     # largeIcon="mdi:home-assistant",
    #     corner=Positions.BOTTOM_LEFT,
    #     seconds=30,
    # )

    # print(response)

    # response = await notifier.async_send(
    #     message="This is a notification message",
    #     title="Notification Title",
    #     id="0",
    #     appTitle="PyTest",
    #     appIcon="mdi:unicorn",
    #     smallIconColor="#FFC107",
    #     image="c:\\temp\\haos.png",
    #     smallIcon="mdi:bell",
    #     # largeIcon="mdi:home-assistant",
    #     corner=Positions.BOTTOM_LEFT.value,
    #     seconds=30,
    # )

    # print(response)

    # response = await notifier.async_send(
    #     message="This is a notification message",
    #     title="Notification Title",
    #     id="0",
    #     appTitle="PyTest",
    #     appIcon="c:\\temp\\haos.png",
    #     smallIconColor="#FFC107",
    #     image="c:\\temp\\haos.png",
    #     smallIcon="mdi:bell",
    #     # largeIcon="mdi:home-assistant",
    #     corner=Positions.BOTTOM_LEFT.value,
    #     seconds=10,
    # )

    # print(response)


    # response = await notifier.async_send(
    #     message="This is a notification message",
    #     title="Notification Title",
    #     id="0",
    #     appTitle="PyTest",
    #     appIcon="mdi:unicorn",
    #     smallIconColor="#FFC107",
    #     image="mdi:home-assistant",
    #     smallIcon="mdi:bell",
    #     # largeIcon="mdi:home-assistant",
    #     corner=Positions.BOTTOM_LEFT.value,
    #     seconds=30,
    # )

    # print(response)

    # response = await notifier.async_send_fixed(
    #     message="This is a notification message",
    #     id="0",
    #     icon="mdi:bell",
    #     textColor="#FFFFFF",
    #     iconColor="#FFFFFF",
    #     borderColor="#FFFFFF",
    #     backgroundColor="#000000",
    #     shape=Shapes.CIRCLE,
    #     expiration="120s",
    #     visible=True,
    # )

    # print(response)


if __name__ == "__main__":
    asyncio.run(main())
