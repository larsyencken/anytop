======
anytop
======

Overview
--------

``anytop`` is a tool for viewing frequency distributions over streaming input.
It reads input line by line, and shows the top elements in the distribution as
they stream in. It is inspired by the excellent command-line tools available
for the Varnish web accelerator.

Usage examples
--------------

Check out which letters words normally start with::

		cut -c 1-1 /usr/share/dict/words | tr [:upper:] [:lower:] | ./anytop.py

Work out the relative distribution of file extensions in a source tree::

		find src -type f | awk -F . '{print $NF}' | ./anytop.py

Exit ``anytop`` by typing CTRL-C.


Memory usage
------------

Anytop uses memory proportional to the number of distinct lines in the input.
If the input keyspace is bounded, then anytop will use limited memory, no
matter how many lines or how long it runs.

When the input keyspace is not bounded, a fixed-size window of lines can be
used with the ``-l`` option.

