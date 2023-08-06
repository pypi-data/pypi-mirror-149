# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['timedelta_nice_format']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'timedelta-nice-format',
    'version': '0.1.0',
    'description': 'PYPI package with 2 functions to convert datetime.timedelta into string with nice format',
    'long_description': '==============================\ntimedelta_nice_format\n==============================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/timedelta_nice_format\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/timedelta_nice_format\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/timedelta_nice_format\n    :target: https://github.com/stas-prokopiev/timedelta_nice_format/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://img.shields.io/pypi/v/timedelta_nice_format\n   :target: https://img.shields.io/pypi/v/timedelta_nice_format\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/timedelta_nice_format\n   :target: https://img.shields.io/pypi/pyversions/timedelta_nice_format\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nOverview.\n=========================\ntimedelta_nice_format is a PYPI package made with only one simple\ngoal to convert time durations into nice human readable format\n\ndatetime.timedelta into nice formatted string\n-----------------------------------------------\n\n.. code-block:: python\n\n    import datetime\n    from timedelta_nice_format import timedelta_nice_format\n\n    start = datetime.datetime.now()\n    # ...\n    # You code here\n    # ...\n    print(\n        "Duration:",\n        timedelta_nice_format(\n            datetime.datetime.now()-start\n        )\n    )\n\nduration in seconds into nice formatted string\n-----------------------------------------------\n\n.. code-block:: python\n\n    import time\n    from timedelta_nice_format import seconds_nice_format\n    start = time.time()\n    # ...\n    # You code here\n    # ...\n    print("Duration:", seconds_nice_format(time.time()-start))\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install timedelta_nice_format\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/timedelta_nice_format/>`_\n    * `GitHub <https://github.com/stas-prokopiev/timedelta_nice_format>`_\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.',
    'author': 'Stanislav Prokopyev',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
