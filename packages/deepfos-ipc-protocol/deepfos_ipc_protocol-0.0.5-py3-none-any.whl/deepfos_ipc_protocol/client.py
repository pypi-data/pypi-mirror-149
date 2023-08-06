import asyncio

from deepfos_ipc_protocol.const import MESSAGE_PROTOCOL, HEADER_PROTOCOL, DETAILLIST_PROTOCOL
from deepfos_ipc_protocol.utils import (
    judge_data_format,
    to_msg_protocol,
    to_header_protocol,
    to_detaillist_protocol,
    logging
)


logger = logging.getLogger(__name__)


class ClientProtocol(asyncio.Protocol):
    def __init__(self, future, loop):
        self.future = future
        self.loop = loop

    def connection_made(self, transport):
        logger.info("Connection made")
        self.transport = transport

    def data_received(self, data):
        if data:
            self.future.set_result(True)
            self.future = self.loop.create_future()
        logger.info("Data received: {!r}".format(data.decode()))

    def connection_lost(self, error):
        if error:
            logger.error('ERROR: {}'.format(error))
        else:
            logger.info('The server closed the connection')


class EchoClientProtocol:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, path: str):
        self.path = path
        self.transport = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.future = self.loop.create_future()

    def _processing_data(self, mtype: str, data):
        '''将传入的数据转为服务端可读取的数据'''
        if mtype in MESSAGE_PROTOCOL:
            buf = to_msg_protocol(mtype, data)
        elif mtype in HEADER_PROTOCOL:
            buf = to_header_protocol(mtype, data)
        elif mtype in DETAILLIST_PROTOCOL:
            buf = to_detaillist_protocol(mtype, data)
        else:
            raise ValueError("Unsupported message type: {}".format(mtype))
        return buf

    async def _create_conn(self):
        '''建立和服务端的连接'''
        if not self.transport:
            transport, protocol = await self.loop.create_unix_connection(
                lambda: ClientProtocol(self.future, self.loop), self.path
            )
            self.transport = transport

    async def _send_msg(self, mtype, message):
        '''向服务端发送数据'''
        await self._create_conn()
        data = self._processing_data(mtype, message)
        self.transport.write(data)
        await self.future

    def send_msg(self, mtype, message):
        judge_data_format(mtype, message)
        self.loop.run_until_complete(self._send_msg(mtype, message))

    def close(self):
        try:
            self.transport.write(b'end')
        finally:
            self.transport.close()
            self.loop.stop()
