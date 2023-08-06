import asyncio
import logging

from data.payload.DataPayloadProcessor import DataPayloadProcessor
from data.websocket.DataWebSocket import DataWebSocket


# todo: need to stop web socket via request or SYS_KILL
class WebSocketRunner:

    def __init__(self, url, payload_processor: DataPayloadProcessor):
        logging.info(f'Websocket runner initialized with URL:{url}')
        self.payload_processor = payload_processor
        self.web_socket = DataWebSocket(url)
        self.loop = asyncio.get_event_loop()

    def fetch_single_payload(self):
        return self.loop.run_until_complete(self.__receive_single_payload())

    async def __receive_single_payload(self):
        async with self.web_socket as ws:
            return await ws.receive()

    def receive_data(self):
        logging.info('Websocket runner set to receiving data')
        asyncio.run(self.__receive_data())

    async def __receive_data(self):
        async with self.web_socket as ws:
            async for payload in ws:
                self.payload_processor.process_payload(payload)
