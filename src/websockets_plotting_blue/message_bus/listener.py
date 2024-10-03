import asyncio

from bluesky_stomp.messaging import MessageContext, MessagingTemplate
from bluesky_stomp.models import Broker, MessageTopic

from websockets_plotting_blue.shared.queue import main_queue

client = MessagingTemplate.for_broker(Broker(host="localhost", port=61613))


def on_message(message: str, context: MessageContext) -> None:
    """
    This function is called when a new message arrives from the broker.
    It puts the message into the queue for the WebSocket to handle.
    """
    print(f"Received message: {message}")
    asyncio.run(main_queue.put(message))  # Put the message in the queue


client.subscribe(MessageTopic(name="my-other-topic"), on_message)
