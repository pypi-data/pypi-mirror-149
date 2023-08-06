==============================
timedelta_nice_format
==============================

.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/timedelta_nice_format
   :target: https://img.shields.io/github/last-commit/stas-prokopiev/timedelta_nice_format
   :alt: GitHub last commit

.. image:: https://img.shields.io/github/license/stas-prokopiev/timedelta_nice_format
    :target: https://github.com/stas-prokopiev/timedelta_nice_format/blob/master/LICENSE.txt
    :alt: GitHub license<space><space>

.. image:: https://img.shields.io/pypi/v/timedelta_nice_format
   :target: https://img.shields.io/pypi/v/timedelta_nice_format
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/timedelta_nice_format
   :target: https://img.shields.io/pypi/pyversions/timedelta_nice_format
   :alt: PyPI - Python Version


.. contents:: **Table of Contents**

Overview.
=========================
timedelta_nice_format is a PYPI package made with only one simple
goal to convert time durations into nice human readable format

datetime.timedelta into nice formatted string
-----------------------------------------------

.. code-block:: python

    import datetime
    from timedelta_nice_format import timedelta_nice_format

    start = datetime.datetime.now()
    # ...
    # You code here
    # ...
    print(
        "Duration:",
        timedelta_nice_format(
            datetime.datetime.now()-start
        )
    )

duration in seconds into nice formatted string
-----------------------------------------------

.. code-block:: python

    import time
    from timedelta_nice_format import seconds_nice_format
    start = time.time()
    # ...
    # You code here
    # ...
    print("Duration:", seconds_nice_format(time.time()-start))

Installation via pip:
======================

.. code-block:: bash

    pip install timedelta_nice_format

Links
=====

    * `PYPI <https://pypi.org/project/timedelta_nice_format/>`_
    * `GitHub <https://github.com/stas-prokopiev/timedelta_nice_format>`_

Contacts
========

    * Email: stas.prokopiev@gmail.com
    * `vk.com <https://vk.com/stas.prokopyev>`_
    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_

License
=======

This project is licensed under the MIT License.