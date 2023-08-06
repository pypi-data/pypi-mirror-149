from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator


@contextmanager
def tempdir() -> Generator[Path, None, None]:
    with TemporaryDirectory() as tmp:
        yield Path(tmp)


def generate_big_sparse_file(path: Path, size) -> Path:
    with path.open('wb+') as file:
        file.seek(size - 1)
        file.write(b"\1")
        file.close()
    return path
