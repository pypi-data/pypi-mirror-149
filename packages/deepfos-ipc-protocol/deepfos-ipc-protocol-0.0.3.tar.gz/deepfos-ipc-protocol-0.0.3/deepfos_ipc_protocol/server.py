import asyncio

from inspect import isfunction
from deepfos_ipc_protocol.utils import resolve_header_protocol, resolve_msg_protocol, resolve_detaillist_protocol
from deepfos_ipc_protocol.const import HEADER_PROTOCOL, MESSAGE_PROTOCOL, DETAILLIST_PROTOCOL


class ServerProtocol(asyncio.Protocol):

    def __init__(self, ins=None, **kwargs) -> None:
        self.ins = ins
        self.data = None
        self.kwargs = kwargs

    def connection_made(self, transport):
        print(id(self))
        peername = transport.get_extra_info("peername")
        print("Connection from {}".format(peername))
        self.transport = transport

    def data_received(self, data):
        mtype = data[0]
        try:
            if mtype in MESSAGE_PROTOCOL:
                self.data = resolve_msg_protocol(data)
                print("Task Meta received: {!r}".format(self.data))
            elif mtype in HEADER_PROTOCOL:
                self.data = resolve_header_protocol(data)
                print("Task Meta received: {!r}".format(self.data))
            elif mtype in DETAILLIST_PROTOCOL:
                self.data = list(resolve_detaillist_protocol(data))
                print("Task Meta received: {!r}".format(self.data))
            else:
                raise ValueError(f"Unsupported mtype: {chr(mtype)}")
            if isinstance(self.ins, type) and hasattr(self.ins, self.kwargs.get("func")):
                func = getattr(self.ins, self.kwargs["func"])
                del self.kwargs["func"]
                func(self.ins, chr(mtype), self.data, **self.kwargs)
            elif isfunction(self.ins):
                self.ins(chr(mtype), self.data, **self.kwargs)
            self.transport.write(b"success")
        except Exception as e:
            self.transport.write(e.__str__().encode("utf8"))
        finally:
            print("Close the client socket")
            self.transport.close()


class EchoServer:
    """
    启动EchoServer服务.
    """

    def __init__(self, path: str, ins=None, **kwargs) -> None:
        self.path = path
        self.ins = ins
        self.kwargs = kwargs

    async def task(self):
        loop = asyncio.get_running_loop()
        server = await loop.create_unix_server(
            lambda: ServerProtocol(self.ins, **self.kwargs), self.path,
        )

        async with server:
            await server.serve_forever()

    def run(self):
        asyncio.run(self.task())
