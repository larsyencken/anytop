======
anytop
======

A tool for viewing frequency distributions over streaming input. `Anytop`
reads input line by line, and shows the top elements in the distribution as
they stream in.

Usage examples
--------------

Check out which letters words normally start with::

		cut -c 1-1 /usr/share/dict/words | tr [:upper:] [:lower:] | ./anytop.py

Work out the relative distribution of file extensions in a source tree::

		find src -type f | awk -F . '{print $NF}' | ./anytop.py

