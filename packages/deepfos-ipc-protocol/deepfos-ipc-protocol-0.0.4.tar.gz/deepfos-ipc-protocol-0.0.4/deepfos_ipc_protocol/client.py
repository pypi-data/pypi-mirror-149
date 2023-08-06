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
    def __init__(self, on_con_lost):
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        logger.info("Connection made")

    def data_received(self, data):
        logger.info("Data received: {!r}".format(data.decode()))

    def connection_lost(self, exc):
        self.on_con_lost.set_result(True)
        logger.info("The server closed the connection")


class EchoClientProtocol:
    def __init__(self, path: str):
        self.path = path

    def _processing_data(self, mtype: str, data):
        '''将传入的数据转为服务端可读取的数据'''
        if mtype in MESSAGE_PROTOCOL:
            buf = to_msg_protocol(mtype, data)
        elif mtype in HEADER_PROTOCOL:
            buf = to_header_protocol(mtype, data)
        elif mtype in DETAILLIST_PROTOCOL:
            buf = to_detaillist_protocol(mtype, data)
        else:
            pass
        return buf

    async def create_conn(self):
        '''建立和服务端的连接'''
        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()
        transport, protocol = await loop.create_unix_connection(
            lambda: ClientProtocol(on_con_lost), self.path
        )
        return on_con_lost, transport

    async def _send_msg(self, mtype, message):
        '''向服务端发送数据'''
        data = self._processing_data(mtype, message)
        on_con_lost, transport = await self.create_conn()
        transport.write(data)
        try:
            await on_con_lost
        finally:
            transport.close()

    def send_msg(self, mtype, message):
        judge_data_format(mtype, message)
        asyncio.run(self._send_msg(mtype, message))
