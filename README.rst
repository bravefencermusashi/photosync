=========
photosync
=========

Synchronize your phone photos easily

Each time you take new photos with your phone and you want to transfer them to your computer you have the same problem:
when did you last transfer them? What should you transfer? How to know if you have already back them up? This program is
here to help solving that problem. It is not really a synchronisation program. Actually it will keep track of already
transferred files, so you copy each file from the source once. When copied, you can sort, move, reorganize them or whatever.
You don't need to keep them as there were transferred to avoid them being transferred again next time. That's why it is not
really a synchronization program.

The "database" is a clear text JSON file optimized for quick finding.

As of my Android phone, photo and video file names have to contain the following pattern : ``(IMG|VID)_YYYYMMDD``.

installation
------------

::

    pip install .

This will install a ``photosync`` script.

usage
-----

::

    usage: photosync [-h] [-d DB] [-v] src dest

    positional arguments:
      src             where are the photos you want to copy
      dest            where you want to copy your photos

    optional arguments:
      -h, --help      show this help message and exit
      -d DB, --db DB  the location of the file that contains information about
                      already transferred photos
      -v, --verbose


