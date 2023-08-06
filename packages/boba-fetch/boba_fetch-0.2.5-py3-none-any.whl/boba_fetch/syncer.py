from contextlib import contextmanager
from dataclasses import dataclass
from multiprocessing.synchronize import Event
from multiprocessing import Event as event, Queue
from os import access, R_OK, W_OK
from pathlib import Path
from queue import Empty
import shlex
from subprocess import run, STDOUT, PIPE, SubprocessError
from threading import Thread
from traceback import format_exc
from typing import Optional, List, ContextManager

from boba_fetch.log import log, thread_name
from boba_fetch.process import SafeProcess
from boba_fetch.rpc import UnixSocketRPCClient


@dataclass(frozen=True)
class WatchParams:
    host: str
    local_dir: Path
    queue: Queue
    delete: bool
    execute_on_complete: Optional[str] = None


@dataclass(frozen=True)
class SyncParams:
    host: str
    local_dir: Path
    remote_path: Path
    delete: bool
    execute_on_complete: Optional[str] = None

    @property
    def on_complete(self) -> Optional[List[str]]:
        return shlex.split(self.execute_on_complete) if self.execute_on_complete else None

    @property
    def name(self) -> str:
        return self.remote_path.name

    @staticmethod
    def from_watch(watch_params: WatchParams, remote_path: Path) -> 'SyncParams':
        return SyncParams(watch_params.host, watch_params.local_dir, remote_path,
                          watch_params.delete, watch_params.execute_on_complete)

    @property
    def no_delete(self) -> 'SyncParams':
        return SyncParams(self.host, self.local_dir, self.remote_path, delete=False)


class Syncer:
    def __init__(self, tracker: UnixSocketRPCClient,
                 halt_flag: Optional[Event] = None,
                 temp_dir: Optional[Path] = None):
        self.halt_flag = halt_flag or event()
        self.sleeping = event()
        self.sleeping.set()
        self.tracker = tracker
        self.temp_dir = temp_dir
        if self.temp_dir and not self.temp_dir.is_dir():
            raise ValueError(f'Temporary directory {self.temp_dir} does not exist!')
        if self.temp_dir and not access(self.temp_dir, R_OK | W_OK):
            raise ValueError(f'No read-write access to temporary directory: {self.temp_dir}')

    def _cmd(self, params: SyncParams) -> List[str]:
        result = ['rsync', '-Pprvzy', '--chmod=D755,F644']
        if self.temp_dir:
            result += ['-T', str(self.temp_dir)]
        if params.delete:
            result += ['--remove-source-files']
        return result + [f'{params.host}:"{str(params.remote_path)}"', str(params.local_dir)]

    def cmd(self, params: SyncParams) -> List[str]:
        return self._cmd(params)

    @contextmanager  # type: ignore # mpypy and typeguard are fighting
    def regular_check_in(self, name) -> ContextManager[None]:  # type: ignore
        stop_check_in = event()
        def repeat():
            while not stop_check_in.is_set():
                self.tracker.check_in(name)
                stop_check_in.wait(timeout=1)
        thread = Thread(target=repeat)
        thread.start()
        try:
            yield
        finally:
            stop_check_in.set()
            thread.join()

    def sync_down(self, params: SyncParams) -> bool:
        proc = SafeProcess(self.cmd(params))
        if not self.halt_flag.is_set():
            for line in proc.run():
                log.info(line)
                if self.halt_flag.is_set():
                    proc.terminate(3)
        return proc.returncode == 0

    def halt(self):
        log.info("Halting")
        self.halt_flag.set()

    @staticmethod
    def execute_on_complete(params: SyncParams) -> None:
        if params.execute_on_complete is not None:
            cmd = params.execute_on_complete.replace('%F', str(params.local_dir / params.name))
            log.info(f'Executing: {cmd}')
            try:
                result = run(shlex.split(cmd), check=False, text=True, stdout=PIPE, stderr=STDOUT)
                log.info(result.stdout)
                log.info(f"Exit Code {result.returncode}")
            except SubprocessError:
                log.error(f"Failed to execute on-complete command: {cmd}")

    def watch_queue(self, watch_params: WatchParams):
        while not self.halt_flag.is_set():
            try:
                remote_path = Path(watch_params.queue.get(timeout=0.5))
                self.sleeping.clear()
                params = SyncParams.from_watch(watch_params, remote_path)
                if not self.tracker.currently_working(params.name):
                    with thread_name(params.name), self.regular_check_in(params.name):
                        log.info(f'Syncing down: {remote_path} ~> {watch_params.local_dir}')
                        self.tracker.start(params.name)
                        try:
                            self.sync_down(params.no_delete)
                            if not self.sync_down(params):  # verification
                                log.error(f"Failed to sync down {params.host}:{params.remote_path}")
                                self.tracker.failed(params.name)
                            else:
                                self.tracker.mark_complete(params.name)
                                log.info(f'Sync complete: {params.local_dir / params.name}')
                                self.execute_on_complete(params)
                                log.info('Post-Sync Task complete.')
                        except Exception:  # pylint: disable=W0703
                            log.error(format_exc())
                            log.error(f"Failed to sync down {params.host}:{params.remote_path}")
                            self.tracker.failed(params.name)
                        finally:
                            self.sleeping.set()
            except Empty:
                continue
