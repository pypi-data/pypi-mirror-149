# Aqueduct 

> aq·ue·duct | \ˈä-kwə-ˌdəkt\

Definition of _aqueduct_

1. a conduit for water
2. a content delivery system for the Swimlane platform

> ([What's new?](CHANGELOG.md))

> ([Testing Steps](TESTING.md))

_Aqueduct_ is a Python package to migrate content from one (source) Swimlane instance to another (destination) instance in reliable and repeatable methodlogy.

## Why?

> Currently we only support transferring of content from one Swimlane instance to another that are the same semantic versioning number

Many Swimlane customers build their own custom content (e.g. Use Cases) to fit their needs. We understand that every organization is different and because of this we have built `aqueduct` to facilitate the _migration_ of this content from one instance to another. During the creation of `aqueduct` we have decided that we want to re-enforce best practices when using Swimlane. This is mainly in the form of **NOT** updating content in your production systems (e.g. destination systems). Changes should strictly be made within a development (source) instance and then migrated to your production instance once your testing is complete.

## Features

You can view all the available parameters for the main Aqueduct class [here](docs/aqueduct.md).

> Each of the listed components below have contain details on how content for that component is synced from one instance to another.

We can sync the following content from one Swimlane instance to another. Please be aware that the order of this list of components is forced whether you are syncing all components (default) or specific components from one Swimlane instance to another.

* [keystore](components/keystore.md)
* [packages](components/packages.md)
* [plugins](components/plugins.md)
* [assets](components/assets.md)
* [workspaces](components/workspaces.md)
* [applications](components/applications.md)
    * [workflows](components/workflows.md)
* [tasks](components/tasks.md)
* [reports](components/reports.md)
* [dashboards](components/dashboards.md)
* [users](components/users.md)
* [groups](components/groups.md)
* [roles](components/roles.md)

## Getting Started

`aqueduct` is a Python-only package hosted on [PyPi](https://pypi.org/project/sw-aqueduct/) and works with Python 3.6 and greater.

```bash
pip install sw-aqueduct
```

## Installation

You can install **aqueduct** on OS X, Linux, or Windows. You can also install it directly from the source. To install, see the commands under the relevant operating system heading, below.

### Prerequisites

The following libraries are required and installed by `aqueduct`:

```
pyyaml==6.0
fire==0.4.0
attrs==21.4.0
pydantic==1.9.0
swimlane==10.5.0
packaging>-21
requests>=2.27.1
```

### macOS, Linux and Windows:

```bash
pip install sw-aqueduct
```

### macOS using M1 processor

```bash
git clone https://github.com/swimlane/aqueduct.git
cd aqueduct

# Satisfy ModuleNotFoundError: No module named 'setuptools_rust'
brew install rust
pip3 install --upgrade pip
pip3 install setuptools_rust

# Back to our regularly scheduled programming . . .  

python setup.py install
```

### Installing from source

```bash
git clone https://github.com/swimlane/aqueduct.git
cd aqueduct
python setup.py install
```

## Usage example (command line)

You can run `aqueduct` from the command line or within your own Python scripts. To use `aqueduct` at the command line simply enter the following in your terminal:

```bash
aqueduct --help
```

```python
from aqueduct import Aqueduct, SwimlaneInstance


sw_source = SwimlaneInstance(
    host="https://10.32.100.xxx",
    username="admin",
    password=""
)

sw_dest = SwimlaneInstance(
    host="https://10.32.100.xxx",
    username="admin",
    password=""
)

aq = Aqueduct(
    source=sw_source,
    destination=sw_dest
)

# this will sync all components listed above.
aq.sync()

# You can specify one or more of them as well.
# example
# aq.sync(components=['applications', 'plugins', 'workspaces', 'roles']
```

## Getting Help

Please create an [issue](https://github.com/swimlane/aqueduct/pulls) if you have questions or run into any issues.

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* Josh Rickard - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/swimlane/aqueduct/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details
