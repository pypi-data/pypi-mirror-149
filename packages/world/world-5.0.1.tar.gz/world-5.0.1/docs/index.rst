==================================
world -- Look up DNS country codes
==================================

.. currentmodule:: world

This package provides a mapping between top-level domain names and their two
letter ISO_ 3166_ country codes.  This script also knows about many
non-geographic, generic, USA-centric, historical, common usage, and reserved
top-level domains.

Both a command line script called ``world`` and a library called ``world``
are available.  The latter can be imported into your Python code for whatever
application you want.

This script takes a list of Internet top-level domain names and prints out
where in the world those domains originate from.  For example::

    $ world tz us
    tz originates from Tanzania, United Republic of
    us originates from United States of America (the)

Reverse look ups are also supported::

    $ world -r united
    Matches for "united":
      ae: United Arab Emirates (the)
      gb: United Kingdom of Great Britain and Northern Ireland (the)
      tz: Tanzania, United Republic of
      uk: United Kingdom (common practice)
      um: United States Minor Outlying Islands (the)
      us: United States of America (the)

Only two-letter country codes are supported, since these are the only ones
that were freely available from the ISO_ 3166_ standard.  However, as of
2015-01-09, even these are no longer freely available in a machine readable
format.


Requirements
============

``world`` requires Python 3.8 or newer.


Documentation
=============

A `simple guide`_ to using the library is available, along with a detailed
`API reference`_.


Project details
===============

* Project home: https://gitlab.com/warsaw/world
* Report bugs at: https://gitlab.com/warsaw/world/issues
* Code hosting: https://gitlab.com/warsaw/world.git
* Documentation: http://world.readthedocs.io/en/latest/

You can install it with `pip`::

    % pip install world

You can grab the latest development copy of the code using git.  The main
repository is hosted on GitLab.  If you have git installed, you can grab
your own branch of the code like this::

    $ git clone https://gitlab.com/warsaw/world.git

You can contact the author via barry@python.org.


Copyright
=========

Copyright (C) 2013-2022 Barry A. Warsaw

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Table of Contents and Index
===========================

* :ref:`genindex`

.. toctree::
    :glob:

    using
    manpage
    apiref
    NEWS


.. _ISO: http://www.iso.org/iso/home.html
.. _3166: http://www.iso.org/iso/home/standards/country_codes/
.. _`simple guide`: using.html
.. _`API reference`: apiref.html
