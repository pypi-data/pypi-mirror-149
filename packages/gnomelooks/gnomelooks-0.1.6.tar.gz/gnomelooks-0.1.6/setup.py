# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getlooks', 'getlooks.tmp.test']

package_data = \
{'': ['*'],
 'getlooks': ['test/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/assets/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/cinnamon/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar-Blue/cinnamon/common-assets/menu/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar-Blue/cinnamon/common-assets/misc/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar-Blue/cinnamon/common-assets/panel/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar-Blue/cinnamon/common-assets/switch/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar-Blue/cinnamon/dark-assets/checkbox/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar-Blue/cinnamon/dark-assets/menu/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar-Blue/cinnamon/dark-assets/misc/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar-Blue/cinnamon/dark-assets/switch/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/gnome-shell/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/gnome-shell/assets/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/gtk-2.0/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/gtk-2.0/apps/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/gtk-2.0/assets/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/gtk-3.0/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/gtk-4.0/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/metacity-1/*',
              'themes/GTK3/4 Themes/Sweet-Ambar-Blue/xfwm4/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/assets/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/cinnamon/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/cinnamon/common-assets/menu/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/cinnamon/common-assets/misc/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/cinnamon/common-assets/panel/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar/cinnamon/common-assets/switch/*',
              'themes/GTK3/4 '
              'Themes/Sweet-Ambar/cinnamon/dark-assets/checkbox/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/cinnamon/dark-assets/menu/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/cinnamon/dark-assets/misc/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/cinnamon/dark-assets/switch/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/gnome-shell/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/gnome-shell/assets/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/gtk-2.0/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/gtk-2.0/apps/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/gtk-2.0/assets/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/gtk-3.0/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/gtk-4.0/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/metacity-1/*',
              'themes/GTK3/4 Themes/Sweet-Ambar/xfwm4/*',
              'themes/GTK3/4 Themes/Sweet-Dark/*',
              'themes/GTK3/4 Themes/Sweet-Dark/assets/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/common-assets/menu/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/common-assets/misc/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/common-assets/panel/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/common-assets/switch/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/dark-assets/checkbox/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/dark-assets/menu/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/dark-assets/misc/*',
              'themes/GTK3/4 Themes/Sweet-Dark/cinnamon/dark-assets/switch/*',
              'themes/GTK3/4 Themes/Sweet-Dark/gnome-shell/*',
              'themes/GTK3/4 Themes/Sweet-Dark/gnome-shell/assets/*',
              'themes/GTK3/4 Themes/Sweet-Dark/gtk-2.0/*',
              'themes/GTK3/4 Themes/Sweet-Dark/gtk-2.0/apps/*',
              'themes/GTK3/4 Themes/Sweet-Dark/gtk-2.0/assets/*',
              'themes/GTK3/4 Themes/Sweet-Dark/gtk-3.0/*',
              'themes/GTK3/4 Themes/Sweet-Dark/gtk-4.0/*',
              'themes/GTK3/4 Themes/Sweet-Dark/metacity-1/*',
              'themes/GTK3/4 Themes/Sweet-Dark/xfwm4/*',
              'themes/GTK3/4 Themes/Sweet/*',
              'themes/GTK3/4 Themes/Sweet/assets/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/common-assets/menu/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/common-assets/misc/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/common-assets/panel/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/common-assets/switch/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/dark-assets/checkbox/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/dark-assets/menu/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/dark-assets/misc/*',
              'themes/GTK3/4 Themes/Sweet/cinnamon/dark-assets/switch/*',
              'themes/GTK3/4 Themes/Sweet/gnome-shell/*',
              'themes/GTK3/4 Themes/Sweet/gnome-shell/assets/*',
              'themes/GTK3/4 Themes/Sweet/gtk-2.0/*',
              'themes/GTK3/4 Themes/Sweet/gtk-2.0/apps/*',
              'themes/GTK3/4 Themes/Sweet/gtk-2.0/assets/*',
              'themes/GTK3/4 Themes/Sweet/gtk-3.0/*',
              'themes/GTK3/4 Themes/Sweet/gtk-4.0/*',
              'themes/GTK3/4 Themes/Sweet/metacity-1/*',
              'themes/GTK3/4 Themes/Sweet/xfwm4/*',
              'tmp/*']}

install_requires = \
['beautifulsoup4', 'colorama', 'lxml', 'requests', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['gnomelooks = getlooks.cli:app']}

setup_kwargs = {
    'name': 'gnomelooks',
    'version': '0.1.6',
    'description': '',
    'long_description': '# Gnome-looks themes cli downloader\n\n**A cli-tool to install and update gnome based Icons, GTK, Cursor themes easily**\n\n### Supported desktop environments\n\n- **Gnone**\n- **Xfce**\n- **KDE Plasma**\n\n![image 1](https://raw.githubusercontent.com/Rishang/gnome-theme-installer/master/.github/images/get.png)\n\n## gnomelooks\n\n\n\n- To Install themes for current user\n        \n        gnomelooks get [THEME-URL]\n\n- To Install themes globally\n\n        sudo gnomelooks get [THEME-URL]\n\n### Installation\n\n    pip3 install -U gnomelooks\n\n## gnomelooks help Page\n\n    ~$ gnomelooks --help\n        Usage: gnomelooks [OPTIONS] COMMAND [ARGS]...\n\n        Theme Installer for Gnome, Xfce4, Kde \n\n        Options:\n        --install-completion  Install completion for the current shell.\n        --show-completion     Show completion for the current shell, to copy it or\n                                customize the installation.\n        --help                Show this message and exit.\n\n        Commands:\n        askenv  | ask deskenv\n        get     | Install new UI themes/icons\n        ls      | List installed themes and icons\n        rm      | Remove installed themes and icons\n        update  | Update installed themes and icons via this tool\n\n## update all themes and icons\n\nRun: `gnomelooks update --themes`\n',
    'author': 'Rishang',
    'author_email': 'rishangbhavsarcs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
