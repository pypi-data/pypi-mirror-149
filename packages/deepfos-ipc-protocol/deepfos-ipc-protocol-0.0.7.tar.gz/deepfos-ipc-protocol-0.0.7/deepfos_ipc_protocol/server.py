import asyncio

from inspect import isfunction
from deepfos_ipc_protocol.utils import (
    resolve_header_protocol,
    resolve_msg_protocol,
    resolve_detaillist_protocol,
    logging
)
from deepfos_ipc_protocol.const import (
    HEADER_PROTOCOL,
    MESSAGE_PROTOCOL,
    DETAILLIST_PROTOCOL
)


logger = logging.getLogger(__name__)


class ServerProtocol(asyncio.Protocol):

    def __init__(self, ins=None, **kwargs) -> None:
        self.ins = ins
        self.data = None
        self.kwargs = kwargs

    def connection_made(self, transport):
        logger.info(id(self))
        peername = transport.get_extra_info("peername")
        logger.info("Connection from {}".format(peername))
        self.transport = transport

    def data_received(self, data):
        if data == b"end":
            self.transport.write(b"end")
            self.transport.close()
            return
        mtype = data[0]
        try:
            if mtype in MESSAGE_PROTOCOL:
                self.data = resolve_msg_protocol(data)
                logger.info("Task Meta received: {!r}".format(self.data))
            elif mtype in HEADER_PROTOCOL:
                self.data = resolve_header_protocol(data)
                logger.info("Task Meta received: {!r}".format(self.data))
            elif mtype in DETAILLIST_PROTOCOL:
                self.data = list(resolve_detaillist_protocol(data))
                logger.info("Task Meta received: {!r}".format(self.data))
            else:
                logger.error(f"Unsupported mtype: {chr(mtype)}")
                raise ValueError(f"Unsupported mtype: {chr(mtype)}")
            if self.ins:
                self.ins(chr(mtype), self.data, **self.kwargs)
            self.transport.write(b"success")
        except Exception as e:
            logger.error(e)
            self.transport.write(e.__str__().encode("utf8"))

    def connection_lost(self, error):
        if error:
            logger.error('SERVER ERROR: {}'.format(error))
        else:
            logger.info('Client Closed')
        super().connection_lost(error)


class EchoServer:
    """
    启动EchoServer服务.
    """

    def __init__(self, path: str, ins=None, **kwargs) -> None:
        self.path = path
        self.ins = ins
        self.kwargs = kwargs
        self.func = self.get_func()

    def get_func(self):
        if isinstance(self.ins, type) and hasattr(self.ins, self.kwargs.get("func")):
            func = getattr(self.ins, self.kwargs["func"])
            del self.kwargs["func"]
            setattr(self.ins, "func", func)
            return self.ins().func
        elif isfunction(self.ins):
            return self.ins
        else:
            return None

    async def task(self):
        loop = asyncio.get_running_loop()
        server = await loop.create_unix_server(
            lambda: ServerProtocol(self.func, **self.kwargs), self.path,
        )
        async with server:
            await server.serve_forever()

    def run(self):
        asyncio.run(self.task())
