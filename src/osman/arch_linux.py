from typing import Iterable, Union
import pathlib
import subprocess

from .installer import Installer
from .pacman import Pacman
from .symbolic_link import SymbolicLink
from .symbolic_linker import SymbolicLinker
from .aur_manager import AurManager
from .directory_maker import DirectoryMaker
from .projects_directory_maker import ProjectsDirectoryMaker
from .vim_plugin_installer import VimPluginInstaller
from .zsh_installer import ZshInstaller


class ArchLinux(Installer):
    def __init__(
        self,
        pacman_packages: Union[str, Iterable[str]],
        aur_packages: Union[str, Iterable[str]],
        vim_plugins: Union[str, Iterable[str]],
        zsh_plugins: Union[str, Iterable[str]],
        font_settings: pathlib.Path,
        root_zshrc: pathlib.Path,
        rc_manager_config: pathlib.Path,
        mullvad_config: pathlib.Path,
        zsh_theme: pathlib.Path,
        zshrc: pathlib.Path,
        pypirc: pathlib.Path,
        xinitrc: pathlib.Path,
        xresources: pathlib.Path,
        condarc: pathlib.Path,
        picom_config: pathlib.Path,
        user_dirs_config: pathlib.Path,
        qtile_config: pathlib.Path,
        vim_config: pathlib.Path,
        ssh_config: pathlib.Path,
        ranger_config: pathlib.Path,
        global_gitignore: pathlib.Path,
        global_gitconfig: pathlib.Path,
        global_git_credentials: pathlib.Path,
        global_git_commit_template: pathlib.Path,
    ) -> None:

        self._pacman = Pacman(pacman_packages)
        self._aur_manager = AurManager(aur_packages)
        self._root_symbolic_linker = SymbolicLinker(
            symbolic_links=(
                SymbolicLink(
                    source=font_settings,
                    destination=pathlib.Path(
                        '/etc',
                        'fonts',
                        'conf.d',
                        '00-font-settings.conf',
                    ),
                ),
                SymbolicLink(
                    source=root_zshrc,
                    destination=pathlib.Path('/root', '.zshrc'),
                ),
                SymbolicLink(
                    source=mullvad_config,
                    destination=pathlib.Path(
                        '/etc',
                        'wireguard',
                        'mullvad-cz4.conf',
                    ),
                ),
                SymbolicLink(
                    source=rc_manager_config,
                    destination=pathlib.Path(
                        '/etc',
                        'NetworkManager',
                        'conf.d',
                        'rc-manager.conf',
                    ),
                ),
            ),
            root=True,
        )

        home = pathlib.Path.home()
        config = home.joinpath('.config')

        self._user_symbolic_linker = SymbolicLinker(
            symbolic_links=(
                SymbolicLink(
                    source=pypirc,
                    destination=home.joinpath('.pypirc'),
                ),
                SymbolicLink(
                    source=zshrc,
                    destination=home.joinpath('.zshrc'),
                ),
                SymbolicLink(
                    source=xinitrc,
                    destination=home.joinpath('.xinitrc'),
                ),
                SymbolicLink(
                    source=xresources,
                    destination=home.joinpath('.Xresources'),
                ),
                SymbolicLink(
                    source=condarc,
                    destination=home.joinpath('.condarc'),
                ),
                SymbolicLink(
                    source=picom_config,
                    destination=home.joinpath('.picom.conf'),
                ),
                SymbolicLink(
                    source=user_dirs_config,
                    destination=config.joinpath('user-dirs.dirs'),
                ),
                SymbolicLink(
                    source=qtile_config,
                    destination=config.joinpath('qtile', 'config.py'),
                ),
                SymbolicLink(
                    source=vim_config,
                    destination=config.joinpath('nvim', 'init.vim'),
                ),
                SymbolicLink(
                    source=ranger_config,
                    destination=config.joinpath('ranger', 'rc.conf'),
                ),
                SymbolicLink(
                    source=ssh_config,
                    destination=home.joinpath('.ssh', 'config'),
                ),
                SymbolicLink(
                    source=global_gitignore,
                    destination=config.joinpath('git', 'ignore'),
                ),
                SymbolicLink(
                    source=global_gitconfig,
                    destination=home.joinpath('.gitconfig'),
                ),
                SymbolicLink(
                    source=global_git_credentials,
                    destination=home.joinpath('.git-credentials'),
                ),
                SymbolicLink(
                    source=global_git_commit_template,
                    destination=home.joinpath('.git-commit-template'),
                ),
            ),
        )
        self._directory_maker = DirectoryMaker(
            directories=(
                pathlib.Path.home().joinpath('.config'),
                pathlib.Path.home().joinpath('.config', 'qtile'),
                pathlib.Path.home().joinpath('.config', 'nvim'),
                pathlib.Path.home().joinpath('.config', 'git'),
                pathlib.Path.home().joinpath('.config', 'ranger'),
                pathlib.Path.home().joinpath('.ssh'),
                pathlib.Path.home().joinpath('downloads'),
                pathlib.Path.home().joinpath('bin'),
            ),
        )
        self._projects_directory_maker = ProjectsDirectoryMaker()
        self._vim_plugin_installer = VimPluginInstaller(vim_plugins)
        self._zsh_installer = ZshInstaller(
            plugins=zsh_plugins,
            theme=SymbolicLink(
                source=zsh_theme,
                destination=pathlib.Path.home().joinpath(
                    '.oh-my-zsh',
                    'themes',
                    'avit-no-icons.zsh-theme',
                ),
            ),
        )

    def install(self) -> None:
        self._directory_maker.install()
        self._pacman.install()
        self._root_symbolic_linker.install()
        self._user_symbolic_linker.install()
        self._projects_directory_maker.install()
        self._vim_plugin_installer.install()
        self._zsh_installer.install()
        # Change the default shell of root.
        subprocess.run(
            args=['sudo', 'chsh', '-s', '/bin/zsh', 'root'],
            check=True,
        )

    def install_user_symbolic_links(self) -> None:
        self._user_symbolic_linker.install()

    def install_projects_directory(self) -> None:
        self._projects_directory_maker.install()
