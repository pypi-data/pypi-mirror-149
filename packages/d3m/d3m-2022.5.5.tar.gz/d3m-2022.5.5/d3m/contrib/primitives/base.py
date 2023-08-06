import os

import d3m
from d3m import utils as d3m_utils
from d3m.metadata import base as metadata_base

# Primitives needs an installation section so that digest is computed and available for the primitive.
if d3m.__version__[0].isdigit():
    installation = [{
        'type': metadata_base.PrimitiveInstallationType.PIP,
        'package': 'd3m',
        'version': d3m.__version__,
    }]
else:
    installation = [{
        'type': metadata_base.PrimitiveInstallationType.PIP,
        'package_uri': 'git+https://gitlab.com/datadrivendiscovery/d3m.git@{git_commit}#egg=d3m'.format(
            git_commit=d3m_utils.current_git_commit(os.path.dirname(__file__)),
        ),
    }]
