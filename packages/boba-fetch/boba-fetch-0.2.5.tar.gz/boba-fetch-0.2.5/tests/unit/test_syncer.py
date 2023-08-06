from multiprocessing import Queue, Event as event
from multiprocessing.synchronize import Event
from pathlib import Path
from subprocess import SubprocessError
from threading import Thread
from time import sleep
from typing import List

from pytest import raises, mark
from pytest_mock import MockerFixture

from boba_fetch.log import log
from boba_fetch.syncer import SyncParams, Syncer, WatchParams
from boba_fetch.tracker import Tracker

from tests.unit.utils import tempdir, generate_big_sparse_file


def test_sync_params() -> None:
    params = SyncParams('test-host',
                        Path.cwd(),
                        Path('/remote/src'),
                        delete=False,
                        execute_on_complete='echo stuff')
    assert params.on_complete == ['echo', 'stuff']
    assert params.name == 'src'


def test_sync_params_from_watch() -> None:
    params = WatchParams('test-host',
                         Path.cwd(),
                         Queue(),
                         delete=False,
                         execute_on_complete='echo stuff')
    sync_params = SyncParams.from_watch(params, Path('/remote/src'))
    assert sync_params.on_complete == ['echo', 'stuff']
    assert sync_params.remote_path == Path('/remote/src')


def test_syncer_init() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            syncer = Syncer(tracker)
            assert syncer.tracker is tracker


def test_syncer_non_existent_temp_dir() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            with raises(ValueError, match=r'Temporary directory .*/\.temp does not exist'):
                Syncer(tracker, temp_dir=(tmp_dir / '.temp'))


def test_syncer_no_read_temp_dir() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            temp_dir = (tmp_dir / '.temp')
            temp_dir.mkdir()
            temp_dir.chmod(0o200)
            with raises(ValueError, match=r'No read-write access to temporary directory: .*/\.temp'):
                Syncer(tracker, temp_dir=temp_dir)


@mark.parametrize('delete,temp_dir,expected', [
    (False, None, ['rsync', '-Pprvzy', '--chmod=D755,F644', 'remote:"/src"', '/dst']),
    (True, None, ['rsync', '-Pprvzy', '--chmod=D755,F644', '--remove-source-files', 'remote:"/src"', '/dst']),
    (True, Path('/tmp'), ['rsync', '-Pprvzy', '--chmod=D755,F644', '-T', '/tmp', '--remove-source-files',
     'remote:"/src"', '/dst']),
])
def test_cmd_generation(delete, temp_dir, expected):
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            syncer = Syncer(tracker, temp_dir=temp_dir)
            params = SyncParams('remote', '/dst', '/src', delete)
            assert syncer.cmd(params) == expected


def local_mock_cmd(self, params: SyncParams) -> List[str]:
    normal = self._cmd(params)
    result = normal[:-2] + [f'{str(params.remote_path)}'] + normal[-1:]
    log.debug(f'Returning CMD: {result}')
    return result


_1GiB = 1024 * 1024 * 1024
_200MiB = 1024 * 1024 * 200


def test_sync_down_basic(mocker: MockerFixture) -> None:
    mocker.patch('boba_fetch.syncer.Syncer.cmd', local_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_file = generate_big_sparse_file(src_dir / 'src.file', _200MiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        dst_file = dst_dir / 'src.file'
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            syncer = Syncer(tracker, temp_dir=stg_dir)
            params = SyncParams('remote', dst_dir, src_file, delete=False)
            assert syncer.sync_down(params)
            assert dst_file.is_file()
            assert dst_file.stat().st_mode == 0o100644
            assert dst_file.stat().st_size == _200MiB


def test_sync_down_terminate(mocker: MockerFixture) -> None:
    mocker.patch('boba_fetch.syncer.Syncer.cmd', local_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_file = generate_big_sparse_file(src_dir / 'src.file', _1GiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        dst_file = dst_dir / 'src.file'
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            halt_flag = event()
            syncer = Syncer(tracker, temp_dir=stg_dir, halt_flag=halt_flag)
            params = SyncParams('remote', dst_dir, src_file, delete=False)

            def run():
                assert not syncer.sync_down(params)
            thread = Thread(target=run)
            thread.start()
            sleep(1)
            halt_flag.set()
            thread.join(1)
            assert not thread.is_alive()
            if dst_file.is_file():
                assert dst_file.stat().st_size < _1GiB


def test_sync_down_no_start(mocker: MockerFixture) -> None:
    mocker.patch('boba_fetch.syncer.Syncer.cmd', local_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_file = generate_big_sparse_file(src_dir / 'src.file', _1GiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        dst_file = dst_dir / 'src.file'
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            halt_flag = event()
            halt_flag.set()
            syncer = Syncer(tracker, temp_dir=stg_dir, halt_flag=halt_flag)
            params = SyncParams('remote', dst_dir, src_file, delete=False)

        def run():
            assert not syncer.sync_down(params)
        thread = Thread(target=run)
        thread.start()
        thread.join(1)
        assert not thread.is_alive()
        assert not dst_file.is_file()


def test_sync_down_directory(mocker: MockerFixture) -> None:
    mocker.patch('boba_fetch.syncer.Syncer.cmd', local_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_subdir = src_dir / 'stuff'
        src_subdir.mkdir()
        generate_big_sparse_file(src_subdir / 'A.file', _200MiB)
        generate_big_sparse_file(src_subdir / 'B.file', _200MiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        dst_file1 = dst_dir / 'stuff' / 'A.file'
        dst_file2 = dst_dir / 'stuff' / 'B.file'
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            syncer = Syncer(tracker, temp_dir=stg_dir)
            params = SyncParams('remote', dst_dir, src_subdir, delete=False)
            assert syncer.sync_down(params)
            assert dst_file1.is_file()
            assert dst_file1.stat().st_size == _200MiB
            assert dst_file2.is_file()
            assert dst_file2.stat().st_size == _200MiB
            assert (dst_dir / 'stuff').stat().st_mode == 0o40755
            assert dst_file1.stat().st_mode == 0o100644
            assert dst_file2.stat().st_mode == 0o100644


def test_sync_down_directory_and_delete(mocker: MockerFixture) -> None:
    mocker.patch('boba_fetch.syncer.Syncer.cmd', local_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_subdir = src_dir / 'stuff'
        src_subdir.mkdir()
        src_file_1 = generate_big_sparse_file(src_subdir / 'A.file', _200MiB)
        src_file_2 = generate_big_sparse_file(src_subdir / 'B.file', _200MiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        dst_file1 = dst_dir / 'stuff' / 'A.file'
        dst_file2 = dst_dir / 'stuff' / 'B.file'
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            syncer = Syncer(tracker, temp_dir=stg_dir)
            params = SyncParams('remote', dst_dir, src_subdir, delete=True)
            assert syncer.sync_down(params)
            assert dst_file1.is_file()
            assert dst_file1.stat().st_size == _200MiB
            assert dst_file2.is_file()
            assert dst_file2.stat().st_size == _200MiB
            assert (dst_dir / 'stuff').stat().st_mode == 0o40755
            assert dst_file1.stat().st_mode == 0o100644
            assert dst_file2.stat().st_mode == 0o100644
            assert not src_file_1.is_file()
            assert not src_file_2.is_file()


def test_on_complete():
    params = SyncParams('test-host',
                        Path.cwd(),
                        Path('/remote/src'),
                        delete=False,
                        execute_on_complete='echo stuff')
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            syncer = Syncer(tracker)
            syncer.execute_on_complete(params)


def test_on_complete_exception(mocker: MockerFixture):
    def error_mock_split(cmd) -> None:
        print(cmd)
        raise SubprocessError('shit happens')
    mocker.patch('shlex.split', error_mock_split)
    params = SyncParams('test-host',
                        Path.cwd(),
                        Path('/remote/src'),
                        delete=False,
                        execute_on_complete='echo stuff')
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            syncer = Syncer(tracker)
            syncer.execute_on_complete(params)


def test_watch_queue_basic(mocker: MockerFixture) -> None:
    mocker.patch('boba_fetch.syncer.Syncer.cmd', local_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_file_1 = generate_big_sparse_file(src_dir / 'A.file', _200MiB)
        src_file_2 = generate_big_sparse_file(src_dir / 'B.file', _200MiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        queue: Queue = Queue()
        queue.put(src_file_1)
        queue.put(src_file_2)
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            params = WatchParams('test-host',
                                 dst_dir,
                                 queue,
                                 delete=False)
            syncer = Syncer(tracker, temp_dir=stg_dir)

            def wait_then_halt():
                sleep(0.1)
                syncer.sleeping.wait(timeout=10)
                sleep(0.1)
                syncer.sleeping.wait(timeout=10)
                syncer.halt()
            thread = Thread(target=wait_then_halt)
            thread.start()
            syncer.watch_queue(params)
            thread.join()
            assert (dst_dir / 'A.file').is_file()
            assert (dst_dir / 'A.file').stat().st_size == _200MiB
            assert (dst_dir / 'B.file').is_file()
            assert (dst_dir / 'B.file').stat().st_size == _200MiB
            assert tracker.completed_at('A.file') != 0.0
            assert tracker.completed_at('B.file') != 0.0


def test_watch_queue_delete(mocker: MockerFixture) -> None:
    mocker.patch('boba_fetch.syncer.Syncer.cmd', local_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_file_1 = generate_big_sparse_file(src_dir / 'A.file', _200MiB)
        src_file_2 = generate_big_sparse_file(src_dir / 'B.file', _200MiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        queue: Queue = Queue()
        queue.put(src_file_1)
        queue.put(src_file_2)
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            params = WatchParams('test-host',
                                 dst_dir,
                                 queue,
                                 delete=True)
            syncer = Syncer(tracker, temp_dir=stg_dir)

            def wait_then_halt():
                sleep(0.1)
                assert syncer.sleeping.wait(timeout=10) # wait for first file
                sleep(0.1)
                assert syncer.sleeping.wait(timeout=10) # wait for second file
                syncer.halt()
            thread = Thread(target=wait_then_halt)
            thread.start()
            syncer.watch_queue(params)
            thread.join()
            assert not (src_dir / 'A.file').is_file()
            assert not (src_dir / 'B.file').is_file()
            assert (dst_dir / 'A.file').is_file()
            assert (dst_dir / 'A.file').stat().st_size == _200MiB
            assert (dst_dir / 'B.file').is_file()
            assert (dst_dir / 'B.file').stat().st_size == _200MiB
            assert tracker.completed_at('A.file') != 0.0
            assert tracker.completed_at('B.file') != 0.0


def test_watch_queue_multiple_syncers(mocker: MockerFixture) -> None:
    mocker.patch('boba_fetch.syncer.Syncer.cmd', local_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_file_1 = generate_big_sparse_file(src_dir / 'A.file', _200MiB)
        src_file_2 = generate_big_sparse_file(src_dir / 'B.file', _200MiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        queue: Queue = Queue()
        queue.put(src_file_1)
        queue.put(src_file_1)
        queue.put(src_file_2)
        queue.put(src_file_2)
        halt = event()
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            params = WatchParams('test-host',
                                 dst_dir,
                                 queue,
                                 delete=False)

            def run_syncer():
                syncer = Syncer(tracker, temp_dir=stg_dir, halt_flag=halt)
                syncer.watch_queue(params)
            thread1 = Thread(target=run_syncer)
            thread1.start()
            thread2 = Thread(target=run_syncer)
            thread2.start()
            sleep(10)
            halt.set()
            thread1.join()
            thread2.join()
            assert (dst_dir / 'A.file').is_file()
            assert (dst_dir / 'A.file').stat().st_size == _200MiB
            assert (dst_dir / 'B.file').is_file()
            assert (dst_dir / 'B.file').stat().st_size == _200MiB
            assert tracker.completed_at('A.file') != 0.0
            assert tracker.completed_at('B.file') != 0.0


def test_watch_queue_error(mocker: MockerFixture) -> None:
    def error_mock_cmd(self, params: SyncParams) -> List[str]:
        raise RuntimeError('shit happens')
    mocker.patch('boba_fetch.syncer.Syncer.cmd', error_mock_cmd)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_file_1 = generate_big_sparse_file(src_dir / 'A.file', _200MiB)
        src_file_2 = generate_big_sparse_file(src_dir / 'B.file', _200MiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        queue: Queue = Queue()
        queue.put(src_file_1)
        queue.put(src_file_2)
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            params = WatchParams('test-host',
                                 dst_dir,
                                 queue,
                                 delete=False)
            syncer = Syncer(tracker, temp_dir=stg_dir)

            def wait_then_halt():
                sleep(0.1)
                syncer.sleeping.wait()
                syncer.halt()
            thread = Thread(target=wait_then_halt)
            thread.start()
            syncer.watch_queue(params)
            thread.join()
            assert tracker.completed_at('A.file') == 0.0
            assert tracker.completed_at('B.file') == 0.0


def test_watch_queue_sync_fail(mocker: MockerFixture) -> None:
    def mock_sync_down_false(_, __) -> bool:
        return False
    mocker.patch('boba_fetch.syncer.Syncer.sync_down', mock_sync_down_false)
    with tempdir() as tmp_dir:
        src_dir = tmp_dir / 'src'
        src_dir.mkdir()
        src_file_1 = generate_big_sparse_file(src_dir / 'A.file', _200MiB)
        src_file_2 = generate_big_sparse_file(src_dir / 'B.file', _200MiB)
        dst_dir = tmp_dir / 'dst'
        dst_dir.mkdir()
        stg_dir = tmp_dir / 'stg'
        stg_dir.mkdir()
        queue: Queue = Queue()
        queue.put(src_file_1)
        queue.put(src_file_2)
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            params = WatchParams('test-host',
                                 dst_dir,
                                 queue,
                                 delete=False)
            syncer = Syncer(tracker, temp_dir=stg_dir)

            def wait_then_halt():
                sleep(0.1)
                syncer.sleeping.wait()
                syncer.halt()
            thread = Thread(target=wait_then_halt)
            thread.start()
            syncer.watch_queue(params)
            thread.join()
            assert tracker.completed_at('A.file') == 0.0
            assert tracker.completed_at('B.file') == 0.0
