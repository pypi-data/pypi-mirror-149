import asyncio

from const import MESSAGE_PROTOCOL, HEADER_PROTOCOL, DETAILLIST_PROTOCOL
from utils import (
    judge_data_format,
    to_msg_protocol,
    to_header_protocol,
    to_detaillist_protocol,
    logging
)


logger = logging.getLogger(__name__)


class ClientProtocol(asyncio.Protocol):

    def __init__(self, ins):
        self.ins = ins

    def connection_made(self, transport):
        logger.info("Connection made")
        self.transport = transport

    def data_received(self, data):
        if data == b"end":
            self.transport.close()
        if data:
            self.ins.future.set_result(data)
        logger.info("Data received: {!r}".format(data.decode()))

    def connection_lost(self, error):
        if error:
            logger.error('ERROR: {}'.format(error))
        else:
            logger.info('The server closed the connection')


class EchoClientProtocol:
    
    transport = None

    def __new__(cls, path, loop):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, path: str, loop):
        self.path = path
        self.loop = loop

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

    async def create_conn(self):
        '''建立和服务端的连接'''
        if not self.transport or self.transport.is_closing():
            transport, protocol = await self.loop.create_unix_connection(
                lambda: ClientProtocol(self), self.path
            )
            self.transport = transport

    async def send_msg(self, mtype, message):
        '''向服务端发送数据'''
        judge_data_format(mtype, message)
        # await self.create_conn()
        self.future = self.loop.create_future()
        data = self._processing_data(mtype, message)
        self.transport.write(data)
        return await self.future

    async def close(self):
        self.future = self.loop.create_future()
        self.transport.write(b'end')
        await self.future
        self.transport.close()
