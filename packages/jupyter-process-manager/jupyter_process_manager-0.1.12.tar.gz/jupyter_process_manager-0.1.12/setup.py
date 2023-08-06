# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyter_process_manager']

package_data = \
{'': ['*']}

install_requires = \
['char>=0.1.2,<0.2.0',
 'ipywidgets>=7.7.0,<8.0.0',
 'local-simple-database>=0.1.10,<0.2.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'round-to-n-significant-digits>=0.1.5,<0.2.0',
 'tabulate>=0.8.9,<0.9.0',
 'yaspin>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'jupyter-process-manager',
    'version': '0.1.12',
    'description': 'Python package with widget to simplify work with many processes in jupyter',
    'long_description': '=======================\njupyter_process_manager\n=======================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/jupyter_process_manager\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/jupyter_process_manager\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/jupyter_process_manager\n    :target: https://github.com/stas-prokopiev/jupyter_process_manager/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://travis-ci.org/stas-prokopiev/jupyter_process_manager.svg?branch=master\n    :target: https://travis-ci.org/stas-prokopiev/jupyter_process_manager\n\n.. image:: https://img.shields.io/pypi/v/jupyter_process_manager\n   :target: https://img.shields.io/pypi/v/jupyter_process_manager\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/jupyter_process_manager\n   :target: https://img.shields.io/pypi/pyversions/jupyter_process_manager\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nOverview.\n=========================\n\nThis is a library which helps working with many processes in a jupyter notebook in a very simple way.\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install jupyter_process_manager\n\nUsage examples\n===================================================================\n\n| Lets say that you want to run some function defined in file **test_function.py**\n| with different arguments as separate processes and have control over them.\n\n\n.. code-block:: python\n\n    # In the file test_function.py\n    def test_just_wait(int_seconds, test_msg=""):\n        if test_msg:\n            print(test_msg)\n        for int_num in range(int_seconds):\n            print(int_num)\n            sleep(1)\n\nThen to run it you just need to do the following:\n\n.. code-block:: python\n\n    from jupyter_process_manager import JPM\n    # OR from jupyter_process_manager import JupyterProcessManager\n    from .test_function import test_just_wait\n    # Create an object which will be handling processes\n    process_manager = JPM(".")\n\n    for seconds_to_wait in range(5, 30, 5):\n        process_manager.add_function_to_processing(\n            test_just_wait,\n            seconds_to_wait,\n            test_msg="hi" * seconds_to_wait\n        )\n\nAll the processes were started and now you can check what is happening with them\n\n**WARNING: Please do NOT try to use functions defined inside jupyter notebook, they won\'t work.**\n\nShow processes output as widget\n--------------------------------------------------------------------------------------------------\n\n.. code-block:: python\n\n    process_manager.show_jupyter_widget(\n        int_seconds_step=2,\n        int_max_processes_to_show=20\n    )\n\n.. image:: images/2.PNG\n\nJPM arguments\n--------------------------------------------------------------------------------------------------\n\n#. **str_dir_for_output**: Directory where to store processes output\n#. **is_to_delete_previous_outputs=True**: Flag If you want to delete outputs for all previous processes in the directory\n\nUsual print output\n--------------------------------------------------------------------------------------------------\n\n.. code-block:: python\n\n    process_manager.wait_till_all_processes_are_over(int_seconds_step=2)\n\n.. image:: images/1.PNG\n\n\nHow to Debug\n--------------------------------------------------------------------------------------------------\n\n.. code-block:: python\n\n    # arguments are the same as in **add_function_to_processing(...)**\n    process_manager.debug_run_of_1_function(func_to_process, *args, **kwargs)\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/jupyter_process_manager/>`_\n    * `readthedocs <https://jupyter_process_manager.readthedocs.io/en/latest/>`_\n    * `GitHub <https://github.com/stas-prokopiev/jupyter_process_manager>`_\n\nProject local Links\n===================\n\n    * `CHANGELOG <https://github.com/stas-prokopiev/jupyter_process_manager/blob/master/CHANGELOG.rst>`_.\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.\n',
    'author': 'Stanislav Prokopyev',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stas-prokopiev/jupyter_process_manager',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
