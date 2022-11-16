import asyncio
import datetime
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

async def run():
    producer = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://eventhub-steven.servicebus.windows.net/;SharedAccessKeyName=FirstPolicy;SharedAccessKey=ReTB+qwXbS7RHUoZrkAoLiJD7+H97ggT6TLP3H7LxV8=;EntityPath=event-hub-1",
                                                             eventhub_name="event-hub-1")
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        now = datetime.datetime.now()
        event_data_batch.add(EventData('Event at %s' % now.time()))


        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())