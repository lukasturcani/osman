from typing import Union, Iterable, Optional
import pathlib
import subprocess

from .installer import Installer


class VimPluginInstaller(Installer):
    def __init__(
        self,
        plugins: Union[str, Iterable[str]],
        base: Optional[pathlib.Path] = None,
    ) -> None:

        if isinstance(plugins, str):
            plugins = (plugins, )

        self._plugins = tuple(plugins)

        if base is None:
            base = pathlib.Path.home()

        self._plugin_directory = base.joinpath(
            '.local',
            'share',
            'nvim',
            'site',
            'pack',
        )

    def install(self) -> None:
        self._plugin_directory.mkdir(parents=True, exist_ok=True)

        for plugin in self._plugins:
            *_, name = plugin.split('/')
            destination = self._plugin_directory.joinpath(
                name,
                'start',
                name,
            )
            subprocess.run(
                args=['git', 'clone', plugin, str(destination)],
                check=True,
            )
