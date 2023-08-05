# findhere

## Overview

`findhere` provides functions that simplify using relative paths in your Python project.

## Main Features

## Installation

```python
pip install findhere
```

## Usage

In the __init__.py of the main repository, add:

```python
import os
import pkg_resources

PROJECT_ROOT = os.path.abspath(
    pkg_resources.resource_filename("${1:project_name}", '..')) \
    if 'PROJECT_ROOT' not in os.environ else os.environ['PROJECT_ROOT']
os.environ['PROJECT_ROOT'] = PROJECT_ROOT

os.environ['CLOUD_ROOT'] = f"gs://{os.path.basename(PROJECT_ROOT)}" \
    if 'CLOUD_ROOT' not in os.environ else os.environ['CLOUD_ROOT']
```

If using datatracker,

```python
os.environ['TRACKER_PATH'] = os.path.join(
    PROJECT_ROOT, os.path.basename(PROJECT_ROOT), 'db.json')
```

If versioneer has been added,

```python
os.environ['VERSION'] = __version__
```

If defining directories for use with a script, use:

```python
os.environ['VERSION'] = '0.1.1'
cloudir, localdir, filedir = init_directories(__file__)
```

## Cite

## Maintainer

[Tarjinder Singh @ tsingh@broadinstitute.org](tsingh@broadinstitute.org)

## Acknowledgements

## Release Notes