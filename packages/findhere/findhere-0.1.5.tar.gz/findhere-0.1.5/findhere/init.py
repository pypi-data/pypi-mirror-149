# %%
import os
import re
import sys

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .findhere import here, set_cloud, reldir, relpath

def init_directories(file_attr, relbase='src'):
    """cloudir, localdir, filedir = init_directories(__file__). Must provide full file path."""
    set_cloud(True)
    cloudir = here(os.path.join('data', reldir(relbase), os.environ['VERSION']))
    localdir = here(os.path.join('data', reldir(relbase), os.environ['VERSION']), local=True)
    filedir = os.path.dirname(file_attr)
    os.environ['FILE'] = relpath(file_attr)
    cloudir = re.sub('\/\.\/', '/', cloudir)
    localdir = re.sub('\/\.\/', '/', localdir)
    return((cloudir, localdir, filedir))
