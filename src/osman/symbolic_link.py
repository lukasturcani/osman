import pathlib


class SymbolicLink:
    def __init__(
        self,
        source: pathlib.Path,
        destination: pathlib.Path,
    ) -> None:

        self._source = source.resolve()
        assert self._source.exists()

        self._destination = destination
        assert self._destination.is_absolute()

    @property
    def source(self) -> pathlib.Path:
        return self._source

    @property
    def destination(self) -> pathlib.Path:
        return self._destination

    def __str__(self):
        return f'SymbolicLink({self._source}, {self._destination})'

    def __repr__(self):
        return str(self)
