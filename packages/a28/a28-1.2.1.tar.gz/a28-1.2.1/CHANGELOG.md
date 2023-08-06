# A28 Changelog

## Unreleased (2022-04-28)

#### New Features

* add missing account alias for arguments
* remove configuration settings as they are in the config module also
* allow the user to specify an environment
* ensure a SystemExit is raised when running directly
* Add vscode editor rules
* added commit git lint gh action ([#22](https://github.com/area28technologies/devkit/issues/22))
#### Fixes

* use the correct setting for the configuration file location
* (devkit): remove all the files at APP_ROOT (including the a28 dire… ([#21](https://github.com/area28technologies/devkit/issues/21))
#### Refactorings

* Change away from using flakehell to using flake9
#### Others

* fix some of the linting errors
* Remove poetry.toml as this should not be stored within the repository

Full set of changes: [`v1.1.0...5790b07`](https://github.com/area28technologies/devkit/compare/v1.1.0...5790b07)

## v1.1.0 (2022-02-10)


Full set of changes: [`v1.0.3...v1.1.0`](https://github.com/area28technologies/devkit/compare/v1.0.3...v1.1.0)

## v1.0.3 (2022-01-07)


Full set of changes: [`v1.0.2...v1.0.3`](https://github.com/area28technologies/devkit/compare/v1.0.2...v1.0.3)

## v1.0.2 (2021-11-05)

#### Others

* bump to 1.0.2
* add .git and .github to the ignored folders for building

Full set of changes: [`v1.0.1...v1.0.2`](https://github.com/area28technologies/devkit/compare/v1.0.1...v1.0.2)

## v1.0.1 (2021-11-03)

#### New Features

* add password argument for account auth
#### Others

* bump version to 1.0.1
* add some missing tests

Full set of changes: [`v1.0.0...v1.0.1`](https://github.com/area28technologies/devkit/compare/v1.0.0...v1.0.1)

## v1.0.0 (2021-11-03)

#### New Features

* add publish command [#1hyw70q](https://github.com/area28technologies/devkit/issues/1hyw70q)
* find or create package with API on init [#1hyw60b](https://github.com/area28technologies/devkit/issues/1hyw60b)
* add account and endpoint options
* add Github Actions for PRs and master push
#### Fixes

* change default path for system commands
* restore tox config and fix lint issues
* security issue with urllib3 < 1.26.5 ([#3](https://github.com/area28technologies/devkit/issues/3))
#### Refactorings

* improve api error handling and fix various typos/config
* lint to pass flake8
* (package): add vim modeline
* (system): add vim modeline
#### Docs

* update README with basic commands
* (package): create proper function documentation
* update changelog to version v0.5.0
#### Others

* add publish workflow
* improve linter/tests config
* bump version to 1.0.0
* add JetBrains IDE config to gitignore
* update test coverage
* (utils): add unit tests for utilities

Full set of changes: [`v0.5.0...v1.0.0`](https://github.com/area28technologies/devkit/compare/v0.5.0...v1.0.0)

## v0.5.0 (2021-10-11)

#### New Features

* (system): add proper type definitions
* (package): allow additional package types to be defined
* (package): add an identifier to the package.json
* (system): add the ability to return the system configuration path
* (system): add the ability to include a configuration path
#### Fixes

* (package): remove dependancy on external index.json
* (package): fix package directory nesting
* (packages): change naming convention to prural for packages
#### Refactorings

* (system): change to use absolute imports
* (cli): use absolute import instead of relative import
* (cli): use absolute import instead of relative import
* (cli): simplified logic in args assignment by changing if statement to or
* separated code block for updating index.json into separate function
* merged json_data assignment with variable declaration
#### Docs

* (package): update function documentation
* (system): add proper type definitions
* updates to contributing doc for setting up environment and improved formatting for readme doc
* add details on how to clean .DS_Store out of zip files
#### Others

* add pytest coverage support
* (system): add the ability to test the system configuration path
* (system): add tests for missing configurations and exists configurations
* (system): add empty check for system configuration
* update coverage report

Full set of changes: [`v0.4.0...v0.5.0`](https://github.com/area28technologies/devkit/compare/v0.4.0...v0.5.0)

## v0.4.0 (2021-06-04)

#### New Features

* add a default package description to package.json
#### Fixes

* remove schema from package name in package.json
* fix command line description of scope parameter
#### Docs

* add simple description for generating a release ([#jt8ny2](https://github.com/area28technologies/devkit/issues/jt8ny2))
* add simple development procedure ([#jt8nbr](https://github.com/area28technologies/devkit/issues/jt8nbr))
#### Others

* add vscode settings for pytest

Full set of changes: [`v0.3.0...v0.4.0`](https://github.com/area28technologies/devkit/compare/v0.3.0...v0.4.0)

## v0.3.0 (2021-05-21)

#### New Features

* add pthe ability to initialize a package ([#8m1ddf](https://github.com/area28technologies/devkit/issues/8m1ddf))
* add short version of package comand ([#jt8760](https://github.com/area28technologies/devkit/issues/jt8760))
* aadd name and scope validation ([#8m1ddf](https://github.com/area28technologies/devkit/issues/8m1ddf))
* add shortened sub command for system ([#jx7pba](https://github.com/area28technologies/devkit/issues/jx7pba))
#### Refactorings

* use consistant naming for packages
#### Others

* release v0.2.0
* break tests out to action based scripts ([#jt944p](https://github.com/area28technologies/devkit/issues/jt944p))
* add args parameter to allow PyTest to run directly ([#8nxr9b](https://github.com/area28technologies/devkit/issues/8nxr9b))

Full set of changes: [`v0.2.0...v0.3.0`](https://github.com/area28technologies/devkit/compare/v0.2.0...v0.3.0)

## v0.2.0 (2021-05-19)

#### New Features

* move actions into separate files
#### Refactorings

* remove erroneous empty lines
#### Others

* add auto-cchangelog to track changes
* remove additional empty lines in imports
* remove local version string in version
* remove local version string in version

Full set of changes: [`v0.1.1...v0.2.0`](https://github.com/area28technologies/devkit/compare/v0.1.1...v0.2.0)

## v0.1.1 (2021-05-18)

#### New Features

* add configuration management
#### Fixes

* fix PEP8 two lines before class
* change doc directory to docs ([#jvb43q](https://github.com/area28technologies/devkit/issues/jvb43q))
* ensure line endings are consistent ([#jvau4k](https://github.com/area28technologies/devkit/issues/jvau4k))
* remove Python 3.10 tests in GitLab [#jv4pu5](https://github.com/area28technologies/devkit/issues/jv4pu5)
#### Others

* add dynamic versioning
* ignore .a28 files when exporting
* add better ci tests
* fix poetry configs in-project command
* add tests for exists and clean actions

Full set of changes: [`v0.1.0...v0.1.1`](https://github.com/area28technologies/devkit/compare/v0.1.0...v0.1.1)

## v0.1.0 (2021-05-12)

#### New Features

* create output directory if it doesn't already exist
* (build): Initial version of the development kit for external developers.
#### Others

* ignore any .a28 packages created
