#!/usr/bin/env python
from setuptools import setup, find_packages

try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
    install_requires = []

setup(
    python_requires=">=3.6",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["iris=NGPIris.cli.base:root"],
    },
    data_files=[('NGPIris', ['config.ini']),
                ('reference', ['reference/covidMetadataAllowedValues.csv', 'reference/covidMetadataTemplate.csv']),
                ('testdata', ['tests/data/test_reads_R1.fasterq','tests/data/test_reads_R1.fastq.gz','tests/data/test.json'])
               ],
)
