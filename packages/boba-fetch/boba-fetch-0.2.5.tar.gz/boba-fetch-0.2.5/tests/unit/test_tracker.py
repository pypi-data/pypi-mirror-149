from time import time, sleep

from boba_fetch.tracker import Tracker

from tests.unit.utils import tempdir


def test_tracker_basics() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            assert tracker.completed_at('some file.txt') == 0.0


def test_tracker_directory_creation() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir / '.track').proxy() as tracker:
            assert tracker.completed_at("test.txt") == 0.0


def test_mark_complete() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            start = time()
            tracker.mark_complete('test.txt')
            assert tracker.completed_at('test.txt') >= start


def test_start() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            tracker.start('test')
            assert (tmp_dir / 'test').is_file()


def test_unfinished() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            tracker.start('test')
            assert tracker.unfinished() == ['test']


def test_failed() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            tracker.start('test')
            assert (tmp_dir / 'test').is_file()
            assert tracker.unfinished() == ['test']
            tracker.failed('test')
            assert not (tmp_dir / 'test').is_file()
            assert not tracker.unfinished()


def test_try_enqueue() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            assert tracker.try_enqueue('test')
            assert not tracker.try_enqueue('test')


def test_try_enqueue_and_start() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            assert tracker.try_enqueue('test')
            tracker.start('test')
            assert not tracker.try_enqueue('test')


def test_start_and_try_enqueue() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            tracker.start('test')
            assert not tracker.try_enqueue('test')


def test_newer_than() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir).proxy() as tracker:
            tracker.mark_complete('test', 16000000)
            assert tracker.newer_than('test', 15000000)


def test_check_in_expiration() -> None:
    with tempdir() as tmp_dir:
        with Tracker(tmp_dir, check_in_timeout=0.2).proxy() as tracker:
            tracker.start('test')
            assert tracker.currently_working('test')
            assert tracker.unfinished() == ['test']
            sleep(0.2)
            assert tracker.unfinished() == []
            assert not tracker.currently_working('test')
