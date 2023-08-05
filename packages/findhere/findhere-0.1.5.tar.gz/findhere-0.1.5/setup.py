#!/usr/bin/env python3

from setuptools import setup, find_packages
import versioneer

with open('README.md') as f:
    readme = f.read()

dependencies = []
with open('requirements.txt', 'r') as f:
    for line in f:
        dependencies.append(line.strip())

setup(
    name='findhere',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Locate paths using relative path names locally and in the Cloud.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Tarjinder Singh',
    author_email='tsingh@broadinstitute.org',
    url='https://github.com/tarjindersingh/findhere',
    license='MIT license',
    python_requires='>=3.7',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=dependencies
)
