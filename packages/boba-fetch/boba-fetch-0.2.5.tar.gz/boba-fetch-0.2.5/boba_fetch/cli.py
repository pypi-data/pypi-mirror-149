from dataclasses import dataclass
from multiprocessing import Process, Event as event, Queue
from multiprocessing.synchronize import Event
from pathlib import Path
from signal import SIGTERM, SIGINT, signal
from tempfile import mkdtemp
from typing import Optional, List
from warnings import simplefilter

import click
from click_path import PathlibPath
import cryptography
from pkg_resources import get_distribution  # type: ignore

from boba_fetch.log import log, thread_name, set_loglevel, DEBUG, INFO
from boba_fetch.poller import RemotePoller
from boba_fetch.rpc import UnixSocketRPCClient
from boba_fetch.syncer import Syncer, WatchParams
from boba_fetch.tracker import Tracker


simplefilter('ignore', cryptography.utils.CryptographyDeprecationWarning)


@dataclass
class BobaConfig:  # pylint: disable=R0902  # dataclasses should be allowed more instance vars
    remote_host: str
    remote_dir: Path
    local_dir: Path
    staging_dir: Path
    tracking_dir: Path
    num_sync_workers: int
    delete_src: bool
    execute_on_complete: Optional[str]
    polling_delay: float
    ssh_config: Path = Path.home() / '.ssh' / '.config'

    def to_watch_params(self, queue: Queue) -> WatchParams:
        return WatchParams(self.remote_host, self.local_dir, queue, self.delete_src,
                           self.execute_on_complete)


def run_poller(config: BobaConfig,
               tracker: UnixSocketRPCClient,
               queue: Queue,
               halt_flag: Event):
    with thread_name("Poller"):
        poller = RemotePoller(config.remote_host, tracker, config.ssh_config)
        poller.poll(config.polling_delay, config.remote_dir, queue, halt_flag)


def start_poller(config: BobaConfig,
                 tracker: UnixSocketRPCClient,
                 queue: Queue,
                 halt_flag: Event) -> Process:
    poller_proc = Process(target=run_poller, args=(config, tracker, queue, halt_flag))
    poller_proc.start()
    return poller_proc


def run_syncer(config: BobaConfig,
               tracker: UnixSocketRPCClient,
               queue: Queue,
               halt_flag: Event,
               index: int):
    with thread_name(f'Syncer {index}'):
        syncer = Syncer(tracker, halt_flag, config.staging_dir)
        syncer.watch_queue(config.to_watch_params(queue))


def start_syncers(config: BobaConfig,
                  tracker: UnixSocketRPCClient,
                  queue: Queue,
                  halt_flag: Event) -> List[Process]:
    syncer_procs = [Process(target=run_syncer,
                            args=(config, tracker,
                                  queue, halt_flag, i)) for i in range(config.num_sync_workers)]
    for proc in syncer_procs:
        proc.start()
    return syncer_procs


@click.command()
@click.version_option(get_distribution('boba-fetch').version)
@click.option('-r', '--remote', required=True,
              help='The remote host to poll for file updates. Must be SSH accessible via public key '
                   'and configured in your ~/.ssh/config')
@click.option('-s', '--src-dir', required=True, type=PathlibPath(exists=False),
              help='The directory on the remote host to check for files to download')
@click.option('-d', '--dst-dir', required=True, type=PathlibPath(exists=True, file_okay=False,
                                                                 dir_okay=True, writable=True,
                                                                 resolve_path=True),
              help='Local directory to sync the files to from the remote host')
@click.option('-g', '--staging-dir', default=None, type=PathlibPath(exists=True, file_okay=False,
                                                                    dir_okay=True, writable=True,
                                                                    resolve_path=True),
              help='Staging directory where files are saved, defaults to randomized temporary directory')
@click.option('-t', '--tracking-dir', required=True, type=PathlibPath(exists=True, file_okay=False,
                                                                      dir_okay=True, writable=True,
                                                                      resolve_path=True),
              help='Tracking directory where we keep track of files that have been synced')
@click.option('-n', '--num-sync-workers', default=3, type=int,
              help='Number of sync workers to use for downloads, defaults to 3')
@click.option('--delete-src', is_flag=True, default=False, help='Indicates to whether to delete the source files on '
                                                                'the remote system')
@click.option('-e', '--execute-on-complete', default=None, help='A command to execute every time a sync is complete')
@click.option('--ssh-config', default=None, type=PathlibPath(exists=True,
                                                                   file_okay=True,
                                                                   dir_okay=False,
                                                                   resolve_path=True),
              help='Path to an SSH configuration file (note that "Include" directives are not yet supported).')
@click.option('-p', '--polling-delay', default=30.0, type=float,
              help='Number of '  # pylint: disable=R0914  # application entry-point, needs local variables
                   'seconds to wait between polls of the remote directory, defaults to 30')
@click.option('--debug', is_flag=True, default=False, help='Turn on debug logging')
def main(remote: str,
         src_dir: Path,
         dst_dir: Path,
         staging_dir: Optional[Path],
         tracking_dir: Path,
         num_sync_workers: int,
         delete_src: bool,
         execute_on_complete: Optional[str],
         ssh_config: Optional[Path],
         polling_delay: float,
         debug: bool):
    set_loglevel(DEBUG if debug else INFO)
    queue: Queue = Queue()
    halt_flag = event()
    config = BobaConfig(remote, src_dir, dst_dir, staging_dir or Path(mkdtemp()),
                        tracking_dir, num_sync_workers, delete_src, execute_on_complete,
                        polling_delay, ssh_config)
    with Tracker(config.tracking_dir).proxy() as tracker:  # type: ignore
        syncer_procs = start_syncers(config, tracker, queue, halt_flag)
        poller_proc = start_poller(config, tracker, queue, halt_flag)

        def handle_signal(_, __):
            halt_flag.set()
        signal(SIGTERM, handle_signal)
        signal(SIGINT, handle_signal)
        poller_proc.join()
        log.info("Poller shutdown complete.")
        for sync_proc in syncer_procs:
            sync_proc.join()
        log.info("Syncer shutdown complete.")
        log.info("Done.")
