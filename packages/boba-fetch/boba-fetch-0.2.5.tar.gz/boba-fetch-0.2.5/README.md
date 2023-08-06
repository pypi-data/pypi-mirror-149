# Boba

A tool for polling a remote source over SSH and syncing new files from said source using `rsync`.

## Setup & Usage

### Installation

`boba-fetch` can be easily installed with `pip`:

```bash
pip3 install boba-fetch
```

### Usage

The most up-to-date instructions for use can be found using `boba-fetch --help`, however, the basic idea is that you need to have a server configured with ssh public key authentication. You should be able to access the server using `ssh <servername>`. Once that's set up, using `boba-fetch` is pretty easy:

``` bash
boba-fetch -r <SERVERNAME> -s /path/to/remote/watched/directory -d /path/to/local/download/directory -g /path/to/local/staging/directory -t /path/to/local/tracking/directory
```

The staging directory should be on the same drive as the download directory to speed up transfers and have the files "just appear" in the right place. The tracking directory should be unique for every configuration of `boba-fetch` that you run because its used to keep track of which files have been downloaded and when, which allows `boba-fetch` to redownload the files if it discovers that they have been 

## Development

### Standards

- Be excellent to each other
- Code coverage must be at 100% for all new code, or a good reason must be provided for why a given bit of code is not covered.
  - Example of an acceptable reason: "There is a bug in the code coverage tool and it says its missing this, but its not".
  - Example of unacceptable reason: "This is just exception handling, its too annoying to cover it".
- The code must pass the following analytics tools. Similar exceptions are allowable as in rule 2.
  - `pylint --disable=C0103,C0111,W1203,R0903,R0913 --max-line-length=120 testudo`
  - `flake8 --max-line-length=120 ...`
  - `mypy --ignore-missing-imports --follow-imports=skip --strict-optional ...`
- All incoming information from users, clients, and configurations should be validated.
- All internal arguments passing should be typechecked during testing with [`typeguard.typechecked`](https://typeguard.readthedocs.io/en/latest/userguide.html#using-the-decorator) or [the import hook](https://typeguard.readthedocs.io/en/latest/userguide.html#using-the-import-hook).

### Development Setup

Using [pdm](https://pdm.fming.dev/) install from inside the repo directory:

```bash
pdm install
```

This will set up a virtualenv which you can always run specific commands with `pdm run ...`.

#### Development

### Testing

All testing should be done with `pytest` which is installed with the `--dev` requirements (`pdm --dev install ...`).

To run all the unit tests, execute the following from the repo directory:

```bash
pdm run pytest
```

This should produce a coverage report in `/path/to/dewey-api/htmlcov/`

While developing, you can use [`watchexec`](https://github.com/watchexec/watchexec) to monitor the file system for changes and re-run the tests:

```bash
watchexec -r -e py,yaml pdm run pytest
```

To run a specific test file:

```bash
pdm run pytest tests/unit/test_cli.py
```

To run a specific test:

```bash
pdm run pytest tests/unit/test_cli.py::test_cli_basics
```

For more information on testing, see the `pytest.ini` file as well as the [documentation](https://docs.pytest.org/en/stable/).
