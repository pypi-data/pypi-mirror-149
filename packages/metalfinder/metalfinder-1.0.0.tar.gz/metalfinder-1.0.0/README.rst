``metalfinder`` is a command-line tool that scans a music directory to find
concerts near a specified location.

Installation
============

Using pip
---------

You can install ``metalfinder`` using pip::

    $ pip install metalfinder

API Providers
=============

Bandsintown
-----------

To use the `Bandsintown`_ API provider, you will need a `Bandsintown App ID`_.
This is your API key and it should be kept private.

.. _Bandsintown: https://bandsintown.com
.. _Bandsintown App ID: https://www.artists.bandsintown.com/support/api-installation

SongKick
--------

The SongKick API provider is not currently implemented. See `issue #3`_ for more
details.

.. _issue #3: https://gitlab.com/baldurmen/metalfinder/-/issues/3

CLI options
===========

Here is an example of how to use ``metalfinder``::

     $ metalfinder -d "/home/foo/Music" -o "/home/foo/metalfinder.atom" -l "Montreal"

The complete CLI parameters can be found below and in the man page::

    Usage:
        metalfinder -d <directory> -o <output> -l <location> -b <app_id> [-c <cache>] [-m <date>] [--verbose]
        metalfinder (-h | --help)
        metalfinder --version

    Options:
        -h  --help                   Show the help screen
        --version                    Output version information
        --verbose                    Run the program in verbose mode
        -d  --directory <directory>  Music directory to scan to create artist list
        -o  --output    <output>     Path to the desired output file. You can either
                                     chose a text file (foo.txt), a JSON file (foo.json)
                                     or an ATOM file (foo.atom)
        -l  --location  <location>   Name of the city to use when looking for concerts
        -b  --bit-appid <app_id>     Bandsintown App ID (API key)
        -c  --cache     <cache>      Path to the cache directory. Defaults to
                                     XDG_CACHE/metalfinder
        -m  --max-date  <date>       Max date in YYYY-MM-DD format (ISO 8601)

Development
=============

Running the test suite
----------------------

Building the man page
---------------------

The man page for ``metalfinder`` can be generated using the ``rst2man`` command
line tool provided by the ``docutils`` project::

    $ rst2man manpage.rst metalfinder.1

License
=======

This project was written by `Louis-Philippe Véronneau`_ and is licensed under
the GNU GPLv3 or any later version.

The code to query Bandsintown comes from the `python-bandsintown`_ project, was
written by Chris Forrette and is licensed under the MIT license.

.. _Louis-Philippe Véronneau: https://veronneau.org
.. _python-bandsintown: https://github.com/chrisforrette/python-bandsintown
