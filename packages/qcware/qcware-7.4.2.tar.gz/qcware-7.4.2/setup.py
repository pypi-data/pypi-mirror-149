# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qcware',
 'qcware.forge',
 'qcware.forge.api_calls',
 'qcware.forge.circuits',
 'qcware.forge.circuits.api',
 'qcware.forge.config',
 'qcware.forge.montecarlo',
 'qcware.forge.montecarlo.api',
 'qcware.forge.montecarlo.nisqAE',
 'qcware.forge.montecarlo.nisqAE.api',
 'qcware.forge.optimization',
 'qcware.forge.optimization.api',
 'qcware.forge.qio',
 'qcware.forge.qio.api',
 'qcware.forge.qml',
 'qcware.forge.qml.api',
 'qcware.forge.qml.types',
 'qcware.forge.qutils',
 'qcware.forge.qutils.api',
 'qcware.forge.test',
 'qcware.forge.test.api',
 'qcware.serialization',
 'qcware.serialization.transforms',
 'qcware.types',
 'qcware.types.optimization',
 'qcware.types.optimization.problem_spec',
 'qcware.types.optimization.problem_spec.utils',
 'qcware.types.optimization.results',
 'qcware.types.optimization.results.utils',
 'qcware.types.optimization.utils',
 'qcware.types.qml',
 'qcware.types.test_strategies']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4.post0',
 'backoff>=1.10.0',
 'colorama>=0.4.4',
 'icontract>=2.5.3',
 'lz4>=3.1.3',
 'networkx>=2.5.1',
 'numpy>=1.21.5,<2.0.0',
 'packaging>=20.9',
 'pydantic>=1.8.2',
 'python-decouple>=3.4',
 'qcware-quasar>=1.0.4',
 'qubovert>=1.2.3',
 'requests>=2.25.1',
 'rich>=12.0',
 'setuptools>=57.1.0',
 'tabulate>=0.8.9',
 'toolz>=0.11.2']

setup_kwargs = {
    'name': 'qcware',
    'version': '7.4.2',
    'description': "The python client for QC Ware's Forge SaaS quantum computing product",
    'long_description': '\n\n.. image:: http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png\n   :alt: logo\n\n\n========================================\nForge Client Library\n========================================\n\nThis package contains functions for easily interfacing with Forge.\n\n\n.. image:: https://badge.fury.io/py/qcware.svg\n   :target: https://badge.fury.io/py/qcware\n   :alt: PyPI version\n\n.. image:: https://pepy.tech/badge/qcware\n   :target: https://pepy.tech/project/qcware\n   :alt: Downloads\n\n.. image:: https://pepy.tech/badge/qcware/month\n   :target: https://pepy.tech/project/qcware/month\n   :alt: Downloads\n\n.. image:: https://circleci.com/gh/qcware/platform_client_library_python.svg?style=svg\n   :target: https://circleci.com/gh/qcware/platform_client_library_python\n   :alt: CircleCI\n\n.. image:: https://readthedocs.org/projects/qcware/badge/?version=latest\n   :target: https://qcware.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n|\n\nInstallation\n============\n\nTo install with pip:\n\n.. code:: shell\n\n   pip install qcware\n\nTo install from source, you must first install `poetry <https://python-poetry.org/docs/>`_.\nThen, execute the following:\n\n.. code:: shell\n\n   git clone https://github.com/qcware/platform_client_library_python.git\n   cd platform_client_library_python\n   poetry build\n   cd dist\n   pip install qcware-7.0.0-py3-none-any.whl\n\n\nAPI Key\n=======\n\nTo use the client library, you will need an API key. You can sign up for one at `https://forge.qcware.com <https://forge.qcware.com>`__.\n\nTo access your API key, log in to `Forge <https://forge.qcware.com>`_ and navigate to the API page. Your API key should be plainly visible there.\n\n\nA Tiny Program\n==============\n\nThe following code snippet illustrates how you might run Forge client code locally. Please make sure that you have installed the client library and obtained an API key before running the Python code presented below.\n\n.. code:: python\n\n    # configuration\n    from qcware.forge.config import set_api_key, set_host\n    set_api_key(\'YOUR-API-KEY-HERE\')\n    set_host(\'https://api.forge.qcware.com\')\n\n    # specify the problem (for more details, see the "Getting Started" Jupyter notebook on Forge)\n    from qcware.forge import optimization\n    from qcware.types import PolynomialObjective, Constraints, BinaryProblem\n\n    qubo = {\n        (0, 0): 1,\n        (0, 1): 1,\n        (1, 1): 1,\n        (1, 2): 1,\n        (2, 2): -1\n    }\n\n    qubo_objective = PolynomialObjective(\n        polynomial=qubo,\n        num_variables=3,\n        domain=\'boolean\'\n    )\n\n    # run a CPU-powered brute force solution\n    results = optimization.brute_force_minimize(\n        objective=qubo_objective,\n        backend=\'qcware/cpu\'\n    )\n    print(results)\n\nIf the client code has been properly installed and configured, the above code should display a result similar to the following:\n\n.. code:: shell\n\n    Objective value: -1\n    Solution: [0, 0, 1]\n\nFor further guidance on running client code to solve machine learning problems, optimization problems, and more, please read through the documentation made available at `https://qcware.readthedocs.io <https://qcware.readthedocs.io/>`_ as well as the Jupyter notebooks made available on `Forge <https://app.forge.qcware.com/>`__.\n',
    'author': 'Vic Putz',
    'author_email': 'vic.putz@qcware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/qcware/platform_client_library_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
