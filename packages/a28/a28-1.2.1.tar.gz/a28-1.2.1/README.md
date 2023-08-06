# Area28 Development Toolkit

The A28 Developer Toolkit provides developers with the tools and documentation necessary to build packages for the Area28 Application and to manage configuration files.

## General information

### Python version

Area28 follows the [VFX Reference Platform](https://vfxplatform.com/) which restricts Python to 3.7.x currently.

### Installation
The A28 Development Kit is published on PyPI and can be installed from there:

```sh
pip install -U a28
```

We also publish beta releases:

```sh
pip install -U --pre a28
```

If you wish to install A28 for development purposes, refer to the contributors guide.

### Documentation
Documentation is available on [GitHub](https://area28technologies.github.io/devkit/).

### Get in touch
Report bugs, suggest features or view the source code on GitHub.

## Coding structure

### Interfaces

- IPlugin
- IApiExtension
- IApplicationExtension
- IChatExtension
- IEventExtension
- IInteractionExtension
- ILoggerExtension
- IMetadataExtension
- IPreferencesExtension
- IRealtimeExtension
- IUiExtension
- IUnitsExtension

### Plugins

Plugins are decorators that can be used to manipulate the payload before being processed or before getting returned.

### Extensions

Extension are used to add additional functionality to the Area28 application. Extensions are broken up into multiple types, defined within the Interfaces list.

## Packaging

Each package has a unique identifier associated with it and is compressed into a .a28 file. Please look at the a28 development kit for details.

### Package structure

```sh
@{provider}
|-- {package}
    |-- extensions
    |   |-- {extensions[]}.py
    |-- scripts
    |   |-- install.py
    |   |-- postinstall.py
    |   |-- preinstall.py
    |   |-- uninstall.py
    |-- plugin
    |   |-- {application specific plugin}
    |-- plugins
    |   |-- {plugin[]}.py
    |-- bin
    |   |--{executable[]}.py
    |-- package.json
```

### Package.json structure

```json
{
    "name": "@area28/unity-application",
    "version": "0.0.4",
    "description": "Detect is running within Unity3D.",
    "homepage": "https://area28.io",
    "keywords": [
        "area28",
        "chat",
        "lowercase",
        "transform"
    ],
    "repository": {
        "type": "git",
        "url": "git+https://github.com/area28/area28.git",
        "directory": "packages/unity-application"
    },
    "author": "Gary Stidston-Broadbent",
    "license": "MIT",
    "bugs": {
        "url": "https://github.com/area28/area28/issues"
    },
    "bin": {
        "myapp": "./bin/lowercase.py"
    },
    "os": [
        "darwin",
        "linux"
    ],
    "cpu": [
        "x64",
        "ia32",
        "!mips"
    ],
    "scripts": {
        "preinstall": "scripts/preinstall.py",
        "install": "scripts/install.py",
        "postinstall": "scripts/postinstall.py",
        "uninstall": "scripts/uninstall.py"
    }
}
```

## Performing package actions

### Authenticate with A28

- `a28 account authenticate -u my.email@example.com`

### Initialize a new package

- `a28 package init --scope my-company --name powerful-plugin --type app my/folder`

This will generate a `package.json` and the folder structure in the given folder ('my/folder')

### Building a package

- `a28 package build --src @area28/chat-logger --dest dist`

This will generate the `.a28` package in `dist/`

### Installing a package locally

- `a28 package install --pkg dist/00000000-0000-0000-0000-00000000-0.0.1.a28`

### Publish a package

- `a28 package publish --pkg dist/00000000-0000-0000-0000-00000000-0.0.1.a28`
