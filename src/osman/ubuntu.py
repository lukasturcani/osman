import pathlib
from typing import Iterable, Union

from .apt import Apt
from .directory_maker import DirectoryMaker
from .installer import Installer
from .pip import Pip3
from .projects_directory_maker import ProjectsDirectoryMaker
from .symbolic_link import SymbolicLink
from .symbolic_linker import SymbolicLinker
from .vim_plugin_installer import VimPluginInstaller
from .zsh_installer import ZshInstaller


class Ubuntu(Installer):
    def __init__(
        self,
        apt_packages: Union[str, Iterable[str]],
        pip_packages: Union[str, Iterable[str]],
        vim_plugins: Union[str, Iterable[str]],
        zsh_plugins: Union[str, Iterable[str]],
        font_settings: pathlib.Path,
        zsh_theme: pathlib.Path,
        zshrc: pathlib.Path,
        gdbinit: pathlib.Path,
        ipython_config: pathlib.Path,
        xresources: pathlib.Path,
        inputrc: pathlib.Path,
        condarc: pathlib.Path,
        user_dirs_config: pathlib.Path,
        qtile_config: pathlib.Path,
        vim_config: pathlib.Path,
        ssh_config: pathlib.Path,
        ranger_config: pathlib.Path,
        global_gitignore: pathlib.Path,
        global_gitconfig: pathlib.Path,
        global_git_commit_template: pathlib.Path,
        qtile_xsession: pathlib.Path,
        xprofile: pathlib.Path,
    ) -> None:

        self._apt = Apt(apt_packages)
        self._pip = Pip3(pip_packages)
        self._root_symbolic_linker = SymbolicLinker(
            symbolic_links=(
                SymbolicLink(
                    source=font_settings,
                    destination=pathlib.Path(
                        "/etc",
                        "fonts",
                        "conf.d",
                        "00-font-settings.conf",
                    ),
                ),
                SymbolicLink(
                    source=qtile_xsession,
                    destination=pathlib.Path(
                        "/usr",
                        "share",
                        "xsessions",
                        "qtile.desktop",
                    ),
                ),
            ),
            root=True,
        )

        home = pathlib.Path.home()
        config = home.joinpath(".config")

        self._user_symbolic_linker = SymbolicLinker(
            symbolic_links=(
                SymbolicLink(
                    source=ipython_config,
                    destination=home.joinpath(
                        ".ipython",
                        "profile_default",
                        "ipython_config.py",
                    ),
                ),
                SymbolicLink(
                    source=zshrc,
                    destination=home.joinpath(".zshrc"),
                ),
                SymbolicLink(
                    source=inputrc,
                    destination=home.joinpath(".inputrc"),
                ),
                SymbolicLink(
                    source=xprofile,
                    destination=home.joinpath(".xprofile"),
                ),
                SymbolicLink(
                    source=gdbinit,
                    destination=home.joinpath(".gdbinit"),
                ),
                SymbolicLink(
                    source=xresources,
                    destination=home.joinpath(".Xresources"),
                ),
                SymbolicLink(
                    source=condarc,
                    destination=home.joinpath(".condarc"),
                ),
                SymbolicLink(
                    source=user_dirs_config,
                    destination=config.joinpath("user-dirs.dirs"),
                ),
                SymbolicLink(
                    source=qtile_config,
                    destination=config.joinpath("qtile", "config.py"),
                ),
                SymbolicLink(
                    source=vim_config,
                    destination=config.joinpath("nvim", "init.vim"),
                ),
                SymbolicLink(
                    source=ranger_config,
                    destination=config.joinpath("ranger", "rc.conf"),
                ),
                SymbolicLink(
                    source=ssh_config,
                    destination=home.joinpath(".ssh", "config"),
                ),
                SymbolicLink(
                    source=global_gitignore,
                    destination=config.joinpath("git", "ignore"),
                ),
                SymbolicLink(
                    source=global_gitconfig,
                    destination=home.joinpath(".gitconfig"),
                ),
                SymbolicLink(
                    source=global_git_commit_template,
                    destination=home.joinpath(".git-commit-template"),
                ),
            ),
        )
        self._directory_maker = DirectoryMaker(
            directories=(
                pathlib.Path.home().joinpath(".config"),
                pathlib.Path.home().joinpath(".config", "qtile"),
                pathlib.Path.home().joinpath(".config", "nvim"),
                pathlib.Path.home().joinpath(".config", "git"),
                pathlib.Path.home().joinpath(".config", "ranger"),
                pathlib.Path.home().joinpath(".ssh"),
                pathlib.Path.home().joinpath("downloads"),
                pathlib.Path.home().joinpath("bin"),
            ),
        )
        self._projects_directory_maker = ProjectsDirectoryMaker()
        self._vim_plugin_installer = VimPluginInstaller(vim_plugins)
        self._zsh_installer = ZshInstaller(
            plugins=zsh_plugins,
        )

    def install(self) -> None:
        self._directory_maker.install()
        self._apt.install()
        self._root_symbolic_linker.install()
        self._user_symbolic_linker.install()
        self._projects_directory_maker.install()
        self._vim_plugin_installer.install()
        self._zsh_installer.install()
        self._pip.install()
