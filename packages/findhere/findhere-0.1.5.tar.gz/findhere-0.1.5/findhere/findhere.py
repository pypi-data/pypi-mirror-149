import os
import sys
import pkg_resources
from hail.utils import hadoop_open

if 'CLOUD' not in os.environ:
    os.environ['CLOUD'] = "false"


def set_cloud(cloud: bool = True):
    """Sets the script to run on the Cloud

    Parameters
    ----------
    cloud : bool, optional
        Flag indicated if the script should operate on Google Cloud, by default True

    See Also
    --------
    here, copen

    Examples
    --------
    >>> set_cloud()
    >>> here('data')
    'gs://findhere/data'
    """
    os.environ['CLOUD'] = "true" if cloud else "false"


def here(path: str = '', local: bool = None) -> str:
    """Returns absolute path when given a relative path

    Returns absolute path relative to local project directory or 
    the Cloud working bucket depending on the CLOUD environment variable
    and the local Boolean flag.

    By default, ``os.environ['CLOUD'] = TRUE`` and ``os.environ['CLOUD'] = False``
    depends if the Cloud or local path is returned.

    The ``local`` flag overwrites the CLOUD environment variable.

    Parameters
    ----------
    path : str
        Relative path to Python project or Cloud bucket
    local : bool, optional
        Read from local project directory if True and read from Cloud directory if False, by default None

    Returns
    -------
    path : str
        Absolute filepath

    Examples
    --------
    >>> here('data')
    '/Users/tsingh/alpha/findhere/data'
    >>> set_cloud()
    >>> here('data')
    'gs://findhere/data'
    """
    abspath = os.path.join(os.environ['CLOUD_ROOT'], path) if os.environ['CLOUD'] == "true" \
        else os.path.join(os.environ['PROJECT_ROOT'], path)
    if local is not None:
        abspath = os.path.join(os.environ['CLOUD_ROOT'], path) if local is False \
            else os.path.join(os.environ['PROJECT_ROOT'], path)
    return(abspath)


def copen(path: str, mode='r'):
    """Open file and return a stream. Able to read from Google bucket directly.

    If the path starts with 'gs', returns a stream to read from the Google bucket;
    otherwise, returns default filestream from build-in open.

    Need to set up Google bucket connector `here
<https://hail.is/docs/0.2/cloud/google_cloud.html#reading-from-google-cloud-storage>`

    Parameters
    ----------
    path : str
        Absolute filepath, can be local or a Cloud path
    mode : str, optional
        specifies the mode in which the file is opened, by default 'r'


    See Also
    --------
    open, hail.utils.hadoop_open


    Examples
    --------
    >>> pd.read_csv(copen(here('data/metadata/ukb.metadata.csv'))) # read locally
    >>> set_cloud()
    >>> pd.read_csv(copen(here('data/metadata/ukb.metadata.csv'))) # read from Cloud
    """
    return(hadoop_open(path, mode) if path[0:2] == 'gs' else open(path, mode))


def is_cloud_path(path):
    return(path[0:3] == 'gs:')


def relpath(abspath, subdir='', infer=True, local=True):
    """Given an absolute path within a project,
    returns relative path to project directory.
    If given subdirectory within project directory, the returned path
    will be relative to that subdirectory. In other words,
    from that directory, what relative path points to the initial file.

    Parameters
    ----------
    abspath : str
        Absolute file path, usually __file__
    subdir : str, optional
        Subdirectory within the project directory, by default ''

    See Also
    --------
    reldir, here

    Examples
    --------
    >>>relpath(__file__, 'src')
    >>>relpath(sys.path[0], '')
    """
    if infer and is_cloud_path(abspath):
        local = False
    else:
        local = True
    return(os.path.relpath(abspath, here(subdir, local)))


def reldir(subdir=''):
    """Returns working directory relative to project directory.
    If given subdirectory within project directory, the returned path
    will be relative to that subdirectory.

    Parameters
    ----------
    subdir : str, optional
        Subdirectory within the project directory, by default ''

    See Also
    --------
    relpath, here

    Examples
    --------
    >>>reldir('src')
    """
    return(relpath(sys.path[0], subdir))
