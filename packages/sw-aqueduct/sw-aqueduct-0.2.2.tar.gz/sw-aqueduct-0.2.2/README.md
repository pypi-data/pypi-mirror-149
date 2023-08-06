# Aqueduct 

> aq·ue·duct | \ˈä-kwə-ˌdəkt\

Definition of _aqueduct_

1. a conduit for water
2. a content delivery system for the Swimlane platform

> ([What's new?](CHANGELOG.md))

> ([Testing Steps](TESTING.md))

_Aqueduct_ is a Python package to migrate content from one (source) Swimlane instance to another (destination) instance in reliable and repeatable methodlogy.

## Table of Contents

* [Why?](#why)
* [Features](#features)
    * [Aqueduct Parameters](docs/aqueduct.md)
* [Getting Started](#getting-started)
* [Usage Examples](#usage-examples)
* [Installation](#installation)
* [Gettting Help](#getting-help)
* [Contributing](#contributing)

## Why?

> Currently we only support transferring of content from one Swimlane instance to another that are the same semantic versioning number

Many Swimlane customers build their own custom content (e.g. Use Cases) to fit their needs. We understand that every organization is different and because of this we have built `aqueduct` to facilitate the _migration_ of this content from one instance to another. During the creation of `aqueduct` we have decided that we want to re-enforce best practices when using Swimlane. This is mainly in the form of **NOT** updating content in your production systems (e.g. destination systems). Changes should strictly be made within a development (source) instance and then migrated to your production instance once your testing is complete.

## Features

> By **default** aqueduct will run __NOT__ perform a live migration of data. You must specify ```live=True``` in order to migrate content.

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

> Please see the [Installation](#installation) section for more information.

## Usage Examples

It is recommended that you use `aqueduct` via a script or within your own Python code base. That being said you can use `aqueduct` via command line. Enter the following in your terminal for more informaton:

```bash
aqueduct --help
```

Before we look at the options available for configuring aqueduct, we must first create two `SwimlaneInstance` objects. One is considered the source instance and the other is the destination instance.

```python
from aqueduct import SwimlaneInstance


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
```

Once we have these instances configured, we can begin to configure `aqueduct`.  You can view all the available parameters for the main Aqueduct class [here](docs/aqueduct.md).

> By default `aqueduct` will **NOT** transfer your content. You must specify the `live=True` parameter in order to actually transfer content.

```python
from aqueduct import Aqueduct

# Below are the default parameters and values when instantiating a Aqueduct object.
aq = Aqueduct(
    source=sw_source,
    destination=sw_dest,
    live=False, 
    offline=False,
    update_reports=False,
    update_dashboards=False,
    continue_on_error=False,
    use_unsupported_version=False,
    force_unsupported_version=False
)
```

Once we have configured out `Aqueduct` class instance we can now sync content from one instance to another. To do this we must call the `sync` method on the `Aqueduct` instance.

```python
# this will sync all components listed above.
aq.sync()
```

By default we will sync all components but you can select which components you want to sync by passing in a list of `components` as an argurment to the `sync` method.

```python
# You can specify one or more of them as well.
aq.sync(components=['applications', 'plugins', 'workspaces', 'roles']
```

You can also include or exclude specific components themselves. Imagine you have an application and a plugin on your source instance that you do not want to transfer to a destination instance. You can specify this in an `exclude` (or `include`) parameter by passing in the following dictionary:

> Please **NOTE** that if you specify a specific component item to exclude you must also provide that same component in the `components` paramter. If you do not then it will run all components and only filter for that application name / plugin name as specified.

```python
aq.sync(components=['applications', 'plugins'], exclude={'applications': ['My Source Application Name'], 'plugins': ['My Source Plugin Name']})
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
