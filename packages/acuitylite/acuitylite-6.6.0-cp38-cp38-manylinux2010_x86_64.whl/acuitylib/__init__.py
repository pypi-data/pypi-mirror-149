import os
from acuitylib.optimize.optimizer import Optimizer
from acuitylib.netwalker import NetWalker
from acuitylib.acuitylog import AcuityLog as Log
from acuitylib.acuitynet import AcuityNet as Net
from acuitylib.acuitynetbuilder import AcuityNetBuilder as Builder
from acuitylib.client import Client as Client
from acuitylib.train.train import Train
import acuitylib.train as train
from acuitylib.xtf import xtf, xrnn
''' Export postprocess
'''
from acuitylib.app.medusa.postprocess.postprocess import PostProcess

def get_version():
    from acuitylib.utils import get_acuity_path, is_binary_package
    if is_binary_package():
        acuity_version_path = os.path.join(get_acuity_path(), 'VERSION')
    else:
        acuity_version_path = os.path.join(get_acuity_path(), 'acuitylib', 'VERSION')
    try:
        with open(acuity_version_path, 'r') as f:
            version = f.readlines()[0].strip('\n')
        return version
    except:
        return None

__version__ = get_version()
