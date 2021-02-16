import pathlib


class SymbolicLink:
    def __init__(
        self,
        source: pathlib.Path,
        destination: pathlib.Path,
    ) -> None:

        self._source = source.resolve()
        assert self._source.exists()

        self._destination = destination.resolve()

    @property
    def source(self) -> pathlib.Path:
        return self._source

    @property
    def destination(self) -> pathlib.Path:
        return self._destination
