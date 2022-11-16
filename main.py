import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore


async def on_event(partition_context, event):
    print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'),
                                                                                 partition_context.partition_id))
    # if "unlabeled" in event.body_as_str(encoding='UTF-8'):
    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)


async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        "DefaultEndpointsProtocol=https;AccountName=camerahub;AccountKey=uGiMxjhSbSJDBNXv1WcEEn2zdeGPryeJo2sHjjC99RxVRB7bTSl09UhkIHFWuQOO4FQMWCbf47IK+AStUT74jw==;EndpointSuffix=core.windows.net",
        "camera")
    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(
        "Endpoint=sb://iothub-ns-friscoioth-22794278-491c13bc0c.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=c89U1Xu0yD0laYivz8fs1urtB8SXb733CwFkwLgr6+0=;EntityPath=friscoiothub",
        consumer_group="$Default", eventhub_name="friscoiothub", checkpoint_store=checkpoint_store)
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event, starting_position="@latest")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())
