from threading import Thread

from boba_fetch.process import SafeProcess

from tests.unit.utils import tempdir


REFUSES_TO_TERMINATE = '''
from signal import SIGTERM, signal

def ignore_sigterm(_, __):
    pass

signal(SIGTERM, ignore_sigterm)

while 42:
    print('test')
'''


def test_uncooperative_process_termination() -> None:
    with tempdir() as tmp_dir:
        script = tmp_dir / 'uncooperative.py'
        script.open('w+').write(REFUSES_TO_TERMINATE)
        proc = SafeProcess(['python', str(script)])
        assert proc.terminate() is None
        for i, line in enumerate(proc.run()):
            assert line == 'test'
            if i == 5:
                proc.terminate(1)
        assert proc.returncode == -9


def test_process_termination() -> None:
    proc = SafeProcess(['sleep', '10'])

    def run():
        for line in proc.run():
            assert not line
    thread = Thread(target=run)
    thread.start()
    proc.started.wait()
    proc.terminate(timeout=1)
    thread.join()
    assert proc.returncode == -15
