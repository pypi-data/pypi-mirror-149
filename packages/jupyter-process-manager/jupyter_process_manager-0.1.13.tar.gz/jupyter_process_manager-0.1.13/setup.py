# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyter_process_manager', 'jupyter_process_manager.gui']

package_data = \
{'': ['*']}

install_requires = \
['char>=0.1.2,<0.2.0',
 'ipywidgets-toggle-buttons>=0.2.3,<0.3.0',
 'ipywidgets>=7.7.0,<8.0.0',
 'local-simple-database>=0.1.10,<0.2.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'round-to-n-significant-digits>=0.1.5,<0.2.0',
 'tabulate>=0.8.9,<0.9.0',
 'timedelta-nice-format>=0.1.0,<0.2.0',
 'yaspin>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'jupyter-process-manager',
    'version': '0.1.13',
    'description': 'Python package with widget to simplify work with many processes in jupyter',
    'long_description': '=======================\njupyter_process_manager\n=======================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/jupyter_process_manager\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/jupyter_process_manager\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/jupyter_process_manager\n    :target: https://github.com/stas-prokopiev/jupyter_process_manager/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://travis-ci.org/stas-prokopiev/jupyter_process_manager.svg?branch=master\n    :target: https://travis-ci.org/stas-prokopiev/jupyter_process_manager\n\n.. image:: https://img.shields.io/pypi/v/jupyter_process_manager\n   :target: https://img.shields.io/pypi/v/jupyter_process_manager\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/jupyter_process_manager\n   :target: https://img.shields.io/pypi/pyversions/jupyter_process_manager\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nOverview.\n=========================\n\nThis is a library which helps working with many processes in a jupyter notebook in a very simple way.\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install jupyter_process_manager\n\nUsage examples\n===================================================================\n\nHow to create create and start processes for **jupyter_process_manager**\n-------------------------------------------------------------------------------------\n\n.. code-block:: python\n\n    from jupyter_process_manager import JupyterProcessManager\n    process_manager = JupyterProcessManager(".")  # "." - path where to store outputs of the processes\n\n    # And functions for processing\n    process_manager.add_function_to_processing(\n        func1, *func1_args,**func1_kwargs)\n    process_manager.add_function_to_processing(\n        func2, *func2_args,**func2_kwargs)\n\n**WARNING: Please do NOT try to use functions defined inside jupyter notebook, they won\'t work.**\n\nJupyterProcessManager arguments:\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n#. **str_dir_for_output**: Directory where to store processes outputs\n#. **is_to_delete_previous_outputs=True**: Flag If you want to delete outputs for all previous processes in the directory\n\n\n\nUsage in Jupyter Notebook\n------------------------------------------------------------\n\nAfter processes were added, you can check what is happening with them\n\n.. code-block:: python\n\n    process_manager\n\n.. image:: images/2.PNG\n\nHow to check output for the processes\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n| Select the process for which you want to see the output.\n| Select which output you want to see.\n| The output will get updated every 2 seconds.\n\nHow to add more processes\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n| You can add as many processes as you want\n| by running the code below in any other jupyter notebook cell\n\n.. code-block:: python\n\n    process_manager.add_function_to_processing(\n        func_new, *func_new_args,**func_new_kwargs)\n\nHow to stop a process\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nTo stop the process, select it and press the orange button to stop it\n\n| When the button to stop the selected process is pushed.\n| KeyboardInterrupt Exception is called for the process\n| If within 5 seconds process is not finished then the process will be killed.\n\nHow to do a debug run without a new process creation\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n.. code-block:: python\n\n    # arguments are the same as in **add_function_to_processing(...)**\n    process_manager.debug_run_of_1_function(func_to_process, *args, **kwargs)\n\nUsage in a console\n============================\n\n.. code-block:: python\n\n    process_manager.wait_till_all_processes_are_over()\n\nYou will see the output like shown below\n\n.. image:: images/1.PNG\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/jupyter_process_manager/>`_\n    * `readthedocs <https://jupyter_process_manager.readthedocs.io/en/latest/>`_\n    * `GitHub <https://github.com/stas-prokopiev/jupyter_process_manager>`_\n\nProject local Links\n===================\n\n    * `CHANGELOG <https://github.com/stas-prokopiev/jupyter_process_manager/blob/master/CHANGELOG.rst>`_.\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.\n',
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
