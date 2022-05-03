import typing
import pathlib
import subprocess

from .installer import Installer


class RangerPluginInstaller(Installer):
    def __init__(
        self,
        plugins: typing.Union[str, typing.Iterable[str]],
        plugin_directory: pathlib.Path =
            pathlib.Path.home().joinpath(
                '.config',
                'ranger',
                'plugins',
            ),
    ) -> None:

        self._plugins = plugins
        self._plugin_directory = plugin_directory

    def install(self) -> None:
        self._plugin_directory.mkdir(parents=True, exist_ok=True)
        for plugin in self._plugins:
            *_, name = plugin.split('/')
            destination = self._plugin_directory.joinpath(name)
            subprocess.run(
                args=['git', 'clone', plugin, str(destination)]
            )
