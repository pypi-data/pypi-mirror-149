from signal import SIGTERM, signal
from string import ascii_letters, digits
from time import time

from pytest import mark
from typeguard import typeguard_ignore

from boba_fetch.rpc import _random_string, UnixSocketRPCServer


def test_random_string() -> None:
    for _ in range(1000):
        assert len(_random_string(32)) == 32
        assert all(c in (ascii_letters + digits) for c in _random_string(32))


@mark.xfail(strict=True, raises=TypeError)
def test_typeguard() -> None:
    assert _random_string('32')


def test_rpc_server() -> None:
    class TestServer(UnixSocketRPCServer):
        def __init__(self, msg: str) -> None:
            self.msg = msg
            UnixSocketRPCServer.__init__(self)

        @UnixSocketRPCServer.serve
        def get_msg(self) -> str:
            return self.msg

    with TestServer('stuff').proxy() as proxy:
        assert proxy.get_msg() == 'stuff'


def test_uncooperative_shutdown() -> None:
    class UncooperativeTestServer(UnixSocketRPCServer):
        def __init__(self, msg: str) -> None:
            self.msg = msg
            UnixSocketRPCServer.__init__(self)

        @UnixSocketRPCServer.serve
        def setup(self) -> None:
            def sigterm_ignore(_, __):
                pass
            signal(SIGTERM, sigterm_ignore)

        @UnixSocketRPCServer.serve
        def stuff(self) -> str:
            return 'stuff'

    with UncooperativeTestServer('stuff').proxy() as proxy:
        proxy.setup()
        shutdown_start = time()

    assert time() - shutdown_start <= 2.0
