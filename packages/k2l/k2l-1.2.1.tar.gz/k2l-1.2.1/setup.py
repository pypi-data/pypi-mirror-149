# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kmacho', 'kswift', 'ktool']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.11.2,<3.0.0', 'kimg4>=0.1.1,<0.2.0', 'pyaes>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['ktool = ktool.ktool_script:main']}

setup_kwargs = {
    'name': 'k2l',
    'version': '1.2.1',
    'description': 'Static MachO/ObjC Reverse Engineering Toolkit',
    'long_description': '<p align="center">\n<img src=".github/svg/logo.png" alt="Logo" width=450px> \n</p>\n<h4 align="center">\nMachO/ObjC Analysis + Editing toolkit.\n</h4>\n<p align="center">\n  <a href="https://github.com/kritantadev/ktool/actions/workflows/tests.yml">\n    <image src="https://github.com/kritantadev/ktool/actions/workflows/tests.yml/badge.svg">\n  </a>\n  <a href="https://ktool.rtfd.io">\n    <image src="https://readthedocs.org/projects/ktool/badge/?version=latest">\n  </a>\n  <a href="https://pypi.org/project/k2l/">\n    <image src="https://badge.fury.io/py/k2l.svg">\n  </a>\n    <br>\n</p>\n    \n<p align="center">\n  <strong><a href="https://ktool.cynder.me/en/latest/ktool.html"> Library Documentation </a></strong>\n  <br>\n</p>\n    \n<img src=".github/tui.png">\n\n### Installation\n\n```shell\n# Installing\npip3 install k2l\n\n# Updating\npip3 install --upgrade k2l\n```\n\n### Usage \n\n```\n> $ ktool\nUsage: ktool [command] <flags> [filename]\n\nCommands:\n\nGUI (Still in active development) ---\n    ktool open [filename] - Open the ktool command line GUI and browse a file\n\nMachO Analysis ---\n    dump - Tools to reconstruct headers and TBDs from compiled MachOs\n    json - Dump image metadata as json\n    cs - Codesigning info\n    kcache - Kernel cache specific tools\n    list - Print various lists (Classlist, etc.)\n    symbols - Print various tables (Symbols, imports, exports)\n    info - Print misc info about the target mach-o\n\nMachO Editing ---\n    insert - Utils for inserting load commands into MachO Binaries\n    edit - Utils for editing MachO Binaries\n    lipo - Utilities for combining/separating slices in fat MachO files.\n\nMisc Utilities ---\n    file - Print very basic info about the MachO\n    img4 - IMG4 Utilities\n    \n\nRun `ktool [command]` for info/examples on using that command\n```\n    \n---\n\nwritten in pure, 100% python for the sake of platform independence when operating on static binaries and libraries. \nthis should run on any and all implementations of python3.\n    \nTested on:\n* Windows/Windows on ARM64\n* MacOS x86/arm64\n* Linux/Linux ARM64\n* iOS (iSH, ssh)\n* Android (Termux)\n* WebAssembly\n* Brython\n    \n#### Credits\n    \nChained fixup processing is currently entirely based on https://github.com/xpcmdshell/bn-chained-fixups\n\n#### Special thanks to\n\nJLevin and *OS Internals for existing\n\narandomdev for guidance + code\n\nBlacktop for their amazing ipsw project: https://github.com/blacktop/ipsw  \n',
    'author': 'cynder',
    'author_email': 'kat@cynder.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
