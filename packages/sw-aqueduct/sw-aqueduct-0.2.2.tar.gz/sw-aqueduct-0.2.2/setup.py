import os

from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'aqueduct', '__meta__' + '.py'), 'r') as f:
    exec(f.read(), about)

PROJECT_URLS = {
    "Documentation": "https://swimlane.com",
    "Changelog": "https://github.com/swimlane/aqueduct/blob/main/CHANGELOG.md",
    "Bug Tracker": "https://github.com/swimlane/aqueduct/issues",
    "Source Code": "https://github.com/swimlane/aqueduct",
    "Funding": "https://github.com/sponsors/msadministrator",
}

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Information Technology",
    "Intended Audience :: System Administrators",
    "Intended Audience :: End Users/Desktop",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Security"
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    packages=find_packages(exclude=['tests*']),
    license=about['__license__'],
    description=about['__description__'],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    project_urls=PROJECT_URLS,
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['swimlane', 'content', 'soar', 'automation'],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],
    python_requires='>=3.6, <4',
    classifiers=CLASSIFIERS,
    package_data={
        'aqueduct':  ['data/logging.yml']
    },
    entry_points={
          'console_scripts': [
              'aqueduct = aqueduct.__main__:main'
          ]
    }
)