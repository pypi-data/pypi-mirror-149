#!/usr/bin/env python3
import pathlib

import setuptools
from neuralspace import VERSION


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

core_requirements = [
    "click~=7.0.0",
    "randomname~=0.1.3",
    "prettytable~=2.1.0",
    "rich~=10.7.0",
    "coloredlogs~=14.0.0",
    "pandas~=1.2.5",
    "PyYAML~=6.0",
    "urllib3~=1.26.5",
    "ruamel.yaml~=0.16",
    "simple-term-menu~=1.3.0",
    "jsonschema~=3.2.0",
    "pykwalify~=1.8.0",
    "aiohttp~=3.6.3",
    "numpy~=1.19.5",
    "requests~=2.27.1",
    "packaging~=21.3"
]

extras = {
    "full": [
        "datasets~=1.18.3"
    ]
}

setuptools.setup(
    name='neuralspace',
    description="A Python CLI for NeuralSpace APIs",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://docs.neuralspace.ai',
    author='Ayushman Dash',
    author_email='ayushman@neuralspace.ai',
    version=VERSION,
    install_requires=core_requirements,
    extras_require=extras,
    python_requires='>=3.7,<3.9',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    include_package_data=True,
    package_data={
        "data": ["*.txt"]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={"console_scripts": ["neuralspace = neuralspace.cli:entrypoint"]},
)
