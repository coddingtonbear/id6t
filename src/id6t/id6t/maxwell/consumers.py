import asyncio
import json
from queue import Empty, Queue

import aioredis

from channels.generic.http import AsyncHttpConsumer
from django.conf import settings


class MaxwellConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        queue = Queue()

        async def async_reader(channel, queue):
            while(await channel.wait_message()):
                event = await channel.get(encoding='utf-8')
                queue.put(event)

        loop = asyncio.get_event_loop()
        await self.send_headers(
            headers=[
                (b'Cache-Control', b'no-cache'),
                (b'Content-Type', b'text/event-stream'),
                (b'Transfer-Encoding', b'chunked'),
            ]
        )
        conn = await aioredis.create_redis(
            (settings.REDIS_HOST, settings.REDIS_PORT, ),
            loop=loop,
        )
        (channel, ) = await conn.subscribe('maxwell.events')
        assert isinstance(channel, aioredis.Channel)
        while True:
            asyncio.ensure_future(async_reader(channel, queue))
            try:
                event = queue.get_nowait()
                payload = "data: %s\n\n" % event
                await self.send_body(payload.encode('utf-8'), more_body=True)
            except Empty:
                pass
            await asyncio.sleep(1)
