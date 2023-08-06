# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['a28']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2021.10.8,<2022.0.0',
 'coloredlogs[color]>=14.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['a28 = a28.cli:main']}

setup_kwargs = {
    'name': 'a28',
    'version': '1.2.0',
    'description': 'A set of resources and tools to help developers create packages for the Area28 application.',
    'long_description': '# Developer Toolkit\n\nDeveloper Toolkit providing developers with the tools and documentation necessary to build packages for the Area28\nApplication.\n\n## Python version\n\nArea28 follows the [VFX Reference Platform](https://vfxplatform.com/) which restricts Python to 3.7.x currently.\n\n## Interfaces\n\n- IPlugin\n- IApiExtension\n- IApplicationExtension\n- IChatExtension\n- IEventExtension\n- IInteractionExtension\n- ILoggerExtension\n- IMetadataExtension\n- IPreferencesExtension\n- IRealtimeExtension\n- IUiExtension\n- IUnitsExtension\n\n## Plugins\n\nPlugins are decorators that can be used to manipulate the payload before being processed or before getting returned.\n\n## Extensions\n\nExtension are used to add additional functionality to the Area28 application. Extensions are broken up into multiple\ntypes, defined within the Interfaces list.\n\n## Packaging\n\nEach package has a unique identifier associated with it and is compressed into a .a28 file. Please look at the a28\ndevelopment kit for details.\n\n### Package structure\n\n```sh\n@{provider}\n|-- {package}\n    |-- extensions\n    |   |-- {extensions[]}.py\n    |-- scripts\n    |   |-- install.py\n    |   |-- postinstall.py\n    |   |-- preinstall.py\n    |   |-- uninstall.py\n    |-- plugin\n    |   |-- {application specific plugin}\n    |-- plugins\n    |   |-- {plugin[]}.py\n    |-- bin\n    |   |--{executable[]}.py\n    |-- package.json\n```\n\n### Package.json structure\n\n```json\n{\n    "name": "@area28/unity-application",\n    "version": "0.0.4",\n    "description": "Detect is running within Unity3D.",\n    "homepage": "https://area28.io",\n    "keywords": [\n        "area28",\n        "chat",\n        "lowercase",\n        "transform"\n    ],\n    "repository": {\n        "type": "git",\n        "url": "git+https://github.com/area28/area28.git",\n        "directory": "packages/unity-application"\n    },\n    "author": "Gary Stidston-Broadbent",\n    "license": "MIT",\n    "bugs": {\n        "url": "https://github.com/area28/area28/issues"\n    },\n    "bin": {\n        "myapp": "./bin/lowercase.py"\n    },\n    "os": [\n        "darwin",\n        "linux"\n    ],\n    "cpu": [\n        "x64",\n        "ia32",\n        "!mips"\n    ],\n    "scripts": {\n        "preinstall": "scripts/preinstall.py",\n        "install": "scripts/install.py",\n        "postinstall": "scripts/postinstall.py",\n        "uninstall": "scripts/uninstall.py"\n    }\n}\n```\n\n### Authenticate with A28\n\n- `a28 account authenticate -u my.email@example.com`\n\n### Initialize a new package\n\n- `a28 package init --scope my-company --name powerful-plugin --type app my/folder`\n\nThis will generate a `package.json` and the folder structure in the given folder (\'my/folder\')\n\n### Building a package\n\n- `a28 package build --src @area28/chat-logger --dest dist`\n\nThis will generate the `.a28` package in `dist/`\n\n### Installing a package locally\n\n- `a28 package install --pkg dist/00000000-0000-0000-0000-00000000-0.0.1.a28`\n\n### Publish a package\n\n- `a28 package publish --pkg dist/00000000-0000-0000-0000-00000000-0.0.1.a28`\n',
    'author': 'Area28 Technologies',
    'author_email': 'dev@area28.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://area28.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
