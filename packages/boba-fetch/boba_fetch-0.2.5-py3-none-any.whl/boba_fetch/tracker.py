from pathlib import Path
from time import time
from typing import Optional, Dict, List, Set

from boba_fetch.log import log
from boba_fetch.rpc import UnixSocketRPCServer


class Tracker(UnixSocketRPCServer):
    def __init__(self, directory: Path, check_in_timeout: float = 5.0) -> None:
        self.working: Dict[str, float] = {}
        self.enqueued: Set[str] = set()
        self.directory = directory
        self.timeout = check_in_timeout
        if not self.directory.is_dir():
            self.directory.mkdir(parents=True, exist_ok=True)
        UnixSocketRPCServer.__init__(self)
        self.thread_name = 'Tracker'

    @UnixSocketRPCServer.serve
    def try_enqueue(self, name: str) -> bool:
        if name not in self.enqueued and not self.currently_working(name):
            log.debug(f'The file [{name}] is not enqueued and not currently being worked. Marking as enqueued.')
            self.enqueued.add(name)
            log.debug(f'The set of enqueued items is: [{list(self.enqueued)}]')
            log.debug(f'The set of items currently being worked is: [{self.unfinished()}]')
            return True
        log.debug(f'The file [{name}] is either marked enqueued or currently being worked.')
        return False

    @UnixSocketRPCServer.serve
    def completed_at(self, name: str) -> float:
        if (self.directory / name).is_file():
            contents = (self.directory / name).open().read().strip()
            log.debug(f'The file [{name}] tracking file contents: {contents}')
            return float(contents) if contents.replace('.', '', 1).isdigit() else 0.0
        log.debug(f'The tracking file for [{name}] does not exist')
        return 0.0

    @UnixSocketRPCServer.serve
    def mark_complete(self, name: str, timestamp: Optional[float] = None) -> None:
        log.debug(f'Marking [{name}] complete')
        (self.directory / name).open('w+').write(str(timestamp or time()))
        self.not_working(name)

    @UnixSocketRPCServer.serve
    def newer_than(self, name: str, timestamp: float) -> bool:
        if self.completed_at(name) >= timestamp:
            log.debug(f'[{name}] was completed at {self.completed_at(name)} which is >= {timestamp}')
        else:
            log.debug(f'[{name}] was completed at {self.completed_at(name)} which is < {timestamp}')
        return self.completed_at(name) >= timestamp

    @UnixSocketRPCServer.serve
    def start(self, name: str) -> None:
        self.check_in(name)
        (self.directory / name).open('w+').write('')
        if name in self.enqueued:
            self.enqueued.remove(name)

    @UnixSocketRPCServer.serve
    def failed(self, name: str) -> None:
        log.debug(f'Marking [{name}] as failed, removing from working set, enqueued, and tracking file')
        (self.directory / name).unlink(missing_ok=True)
        self.not_working(name)
        log.debug(f'The set of enqueued items is: [{list(self.enqueued)}]')
        log.debug(f'The set of items currently being worked is: [{self.unfinished()}]')

    def not_working(self, name: str) -> None:
        if name in self.working:
            del self.working[name]
        if name in self.enqueued:
            self.enqueued.remove(name)

    def clean(self) -> None:
        now = time()
        for name in [n for n, c in self.working.items() if now - c >= self.timeout]:
            self.failed(name)

    @UnixSocketRPCServer.serve
    def check_in(self, name: str) -> None:
        log.debug(f'Checking in for [{name}]')
        self.clean()
        self.working[name] = time()

    @UnixSocketRPCServer.serve
    def currently_working(self, name: str) -> bool:
        return name in self.working and time() - self.working[name] <= self.timeout

    @UnixSocketRPCServer.serve
    def unfinished(self) -> List[str]:
        self.clean()
        return list(self.working)
