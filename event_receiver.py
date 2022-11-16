import asyncio
import datetime
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore


async def on_event(partition_context, event):
    # Print the event data.
    print("Current time: %s" % datetime.datetime.now().time())
    print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)

async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string("DefaultEndpointsProtocol=https;AccountName=storageforsteven;AccountKey=w6Fue+ARWswivcnKbYsuMK6uMF1061GUiJhrqcTY9Sql+8u1ksYDFfxLQPzDqUInNLIvL+SaDAzp+AStPllR0g==;EndpointSuffix=core.windows.net",
                                                                  "test")

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string("Endpoint=sb://eventhub-steven.servicebus.windows.net/;SharedAccessKeyName=FirstPolicy;SharedAccessKey=ReTB+qwXbS7RHUoZrkAoLiJD7+H97ggT6TLP3H7LxV8=;EntityPath=event-hub-1",
                                                           consumer_group="$Default", eventhub_name="event-hub-1", checkpoint_store=checkpoint_store)
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event,  starting_position="@latest")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())