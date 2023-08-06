from multiprocessing import Queue, Event as event
from multiprocessing.synchronize import Event
from pathlib import Path
from typing import Optional, Tuple, List

from fabric import Connection, Config
from invoke.exceptions import UnexpectedExit

from boba_fetch.log import log
from boba_fetch.rpc import UnixSocketRPCClient


class RemotePoller:
    def __init__(self, remote: str, tracker: UnixSocketRPCClient,
                 ssh_config: Optional[Path] = None) -> None:
        self.remote = remote
        self.tracker = tracker
        self._ssh_config = Config(runtime_ssh_path=(ssh_config or Path.home() / '.ssh' / 'config'))
        self._connection: Optional[Connection] = None

    @staticmethod
    def is_float(candidate: str) -> bool:
        return candidate.replace('.', '', 1).isdigit()

    @staticmethod
    def _process(cand: List[str]) -> Optional[Tuple[float, Path]]:
        if RemotePoller.is_float(cand[0]):
            return float(cand[0]), Path(cand[1])
        return None

    @property
    def connection(self) -> Connection:
        if self._connection is None or not self._connection.is_connected:
            self._connection = Connection(self.remote, config=self._ssh_config)
        return self._connection

    @staticmethod
    def ls(directory: Path) -> str:
        return f"find '{str(directory)}' -mindepth 1 -maxdepth 1 -printf '%T@ %p\n'"

    def find_new_files(self, directory: Path) -> List[Tuple[float, Path]]:
        try:
            results = self.connection.run(self.ls(directory), hide=True).stdout.split('\n')
            files = [RemotePoller._process(line.split(' ', 1)) for line in results if line]
            return [f for f in files if f is not None]
        except (OSError, ValueError) as exc:
            log.warning(f"Unable to connect to {self.remote}: {exc}")
        except UnexpectedExit as exc:
            cmd = self.ls(directory).replace('\n', '\\n')
            log.warning(f"Unable to execute `{cmd}` on {self.remote}: {exc}")
        return []

    def poll(self, delay: float, directory: Path, queue: Queue, halt_flag: Optional[Event] = None) -> None:
        halt_flag = halt_flag or event()
        while not halt_flag.is_set():
            log.info('Polling for new files')
            for mtime, new_file in self.find_new_files(directory):
                if not self.tracker.newer_than(new_file.name, mtime) and self.tracker.try_enqueue(new_file.name):
                    log.info(f'    Enqueuing: {new_file}')
                    queue.put(new_file)
            log.info('Poll Complete')
            halt_flag.wait(timeout=delay)
