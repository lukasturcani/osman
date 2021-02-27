from typing import Union, Iterable
import pathlib
import subprocess

from .installer import Installer
from .symbolic_link import SymbolicLink
from .symbolic_linker import SymbolicLinker


class ZshInstaller(Installer):
    def __init__(
        self,
        plugins: Union[str, Iterable[str]],
        theme: SymbolicLink,
    ) -> None:

        if isinstance(plugins, str):
            plugins = (plugins, )

        self._plugins = tuple(plugins)

        self._symbolic_linker = SymbolicLinker(
            symbolic_links=theme,
        )
        self._plugin_directory = pathlib.Path.home().joinpath(
            '.oh-my-zsh',
            'plugins',
        )

    def install(self) -> None:
        self._install_oh_my_zsh()
        self._install_plugins()
        self._symbolic_linker.install()

    def _install_plugins(self) -> None:
        for plugin in self._plugins:
            *_, name = plugin.split('/')
            destination = str(self._plugin_directory.joinpath(name))
            subprocess.run(
                args=['git', 'clone', plugin, destination],
                check=True,
            )

    def _install_oh_my_zsh(self) -> None:

        install_script = str(pathlib.Path.home().joinpath(
            'install-oh-my-zsh.sh',
        ))

        subprocess.run(
            args=[
                'curl',
                (
                    'https://raw.githubusercontent.com/'
                    'ohmyzsh/ohmyzsh/master/tools/install.sh'
                ),
                '-o',
                install_script,
            ],
            check=True,
        )
        subprocess.run(
            args=['sh', install_script],
            env={
                'CHSH': 'yes',
                'KEEP_ZSHRC': 'yes',
                'RUNZSH': 'no',
                'HOME': str(pathlib.Path.home()),
            },
            check=True,
        )
