Live ISS Tracker
================

.. image:: https://gitlab.com/manojm18/liveisstracker/badges/develop/pipeline.svg?maxAge=1
    :target: https://gitlab.com/manojm18/liveisstracker
    :alt: LiveISStracker CI status

.. image:: https://img.shields.io/gitlab/v/release/manojm18/liveisstracker?sort=date
   :target: https://gitlab.com/manojm18/liveisstracker
   :alt: LiveISStracker release



A command line utility to get stats from International Space Station.


.. code:: bash

    Usage: liveisstracker [OPTIONS]

    liveisstracker can get location,speed and pass-over country based on
    current location of International Space Station

    Options:
    -i, --get-iss-location       Get the current location of International Space
                                   Station + Google MAP URL

    -s, --get-iss-speed          Get the current ground speed of International
                                   Space Station

    -c, --get-country            Get the country above which the ISS is current
                                   passing over

    -p, --plot-iss FILENAME.png  Plot the current position of International
                                   Space Station on a map

    -h, --help                   Show this message and exit.


Get stats from International Space Station

.. code:: bash

   $ liveisstracker -i -s
   Timestamp (UTC): 2021-11-17 15:52:05 ISS is at Lat:24.6399 Lon:30.1919
   https://maps.google.com/?q=24.6399,30.1919&ll=24.6399,30.1919&z=3
   Ground Speed of International Space Station is ~ 24833.19 Km/h


Installation
------------

Install ``liveisstracker`` using ``pip``:

.. code:: bash

    $ pip install liveisstracker --upgrade --no-cache-dir



Requirements
------------

* `Python <https://www.python.org>`_ >= 3.6
* `Pandas <https://github.com/pydata/pandas>`_ (tested to work with 1.1.5)
* `Numpy <http://www.numpy.org>`_ = 1.15.4
* `geopy <https://pypi.org/project/geopy/>`_ = 1.20.0
* `geographiclib <https://pypi.org/project/geographiclib/>`_ = 1.50
* `plotly <https://pypi.org/project/plotly/>`_ = 5.3.1



