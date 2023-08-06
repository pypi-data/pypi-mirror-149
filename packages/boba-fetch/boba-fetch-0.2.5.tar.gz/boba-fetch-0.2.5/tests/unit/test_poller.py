from multiprocessing import Queue, Process, Event as event
from pathlib import Path
from time import sleep

from pytest import mark

from boba_fetch.poller import RemotePoller
from boba_fetch.tracker import Tracker

from tests.unit.utils import tempdir, generate_big_sparse_file


@mark.parametrize('candidate,expected', [
    ('1', True),
    ('1.0', True),
    ('r', False),
    ('1.0.', False)
])
def test_is_float(candidate, expected) -> None:
    assert RemotePoller.is_float(candidate) == expected


@mark.parametrize('candidate,expected', [
    (['a', 'b'], None),
    (['1.5', 'stuff'], (1.5, Path('stuff'))),
    (['a', 'b', 'c'], None),
    (['1.5', 'stuff', 'more?'], (1.5, Path('stuff'))),
])
def test_process(candidate, expected) -> None:
    assert RemotePoller._process(candidate) == expected


def test_basic_polling() -> None:
    # NOTE: This test requires localhost SSH access, there's no way around this
    with tempdir() as tmp_dir:
        remote_dir = tmp_dir / 'stuff'
        remote_dir.mkdir()
        generate_big_sparse_file(remote_dir / 'A.file', 1024 * 1024)
        generate_big_sparse_file(remote_dir / 'B.file', 1024 * 1024)
        generate_big_sparse_file(remote_dir / 'C.file', 1024 * 1024)
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            poller = RemotePoller('localhost', tracker)
            new_files = set(f for _, f in poller.find_new_files(remote_dir))
            assert remote_dir / 'A.file' in new_files
            assert remote_dir / 'B.file' in new_files
            assert remote_dir / 'C.file' in new_files


def test_polling_exec_error() -> None:
    # NOTE: This test requires localhost SSH access, there's no way around this
    with tempdir() as tmp_dir:
        remote_dir = tmp_dir / 'stuff'
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            poller = RemotePoller('localhost', tracker)
            assert not set(f for _, f in poller.find_new_files(remote_dir))


def test_polling_conn_error() -> None:
    # NOTE: This test requires localhost SSH access, there's no way around this
    with tempdir() as tmp_dir:
        remote_dir = tmp_dir / 'stuff'
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            poller = RemotePoller('localhosty', tracker)
            assert not set(f for _, f in poller.find_new_files(remote_dir))


def test_repeated_polling() -> None:
    with tempdir() as tmp_dir:
        remote_dir = tmp_dir / 'stuff'
        remote_dir.mkdir()
        generate_big_sparse_file(remote_dir / 'A.file', 1024)
        generate_big_sparse_file(remote_dir / 'B.file', 1024)
        generate_big_sparse_file(remote_dir / 'C.file', 1024)
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            queue: Queue = Queue()
            poller = RemotePoller('localhost', tracker)
            halt_flag = event()

            def queue_consume():
                for _ in range(3):
                    new_file = queue.get()
                    tracker.start(new_file.name)
                    assert new_file in {remote_dir / 'A.file', remote_dir / 'B.file', remote_dir / 'C.file'}
                    tracker.mark_complete(new_file.name)
                sleep(0.2)
                (remote_dir / 'C.file').touch()
                new_file = queue.get()
                assert new_file == remote_dir / 'C.file'
                tracker.mark_complete(new_file.name)
                sleep(0.2)
                halt_flag.set()
            proc = Process(target=queue_consume)
            proc.start()
            poller.poll(0.1, remote_dir, queue, halt_flag=halt_flag)
            proc.join(timeout=1)
