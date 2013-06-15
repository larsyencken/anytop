======
anytop
======

.. image:: https://travis-ci.org/larsyencken/anytop.png

Overview
--------

``anytop`` is a tool for viewing frequency distributions over streaming input.
It reads input line by line, and shows the top elements in the distribution as
they stream in. It is inspired by the excellent command-line tools available
for the Varnish web accelerator.

``anytop`` is designed to work within a shell flow, allowing you to easily
modify the data streaming in with tools such as ``cut``, ``sed`` and ``tr``.
Get usage help by typing ``anytop --help``. To exit ``anytop``, type CTRL-C.

Example: dictionary words
-------------------------

Get the distribution of word starting with each different letter from the
dictionary::

    cut -c 1-1 /usr/share/dict/words | tr [:upper:] [:lower:] | anytop

.. image:: http://media.quietlyamused.org.s3.amazonaws.com/anytop/img/anytop-dict.png

Looks like ``s``, ``p`` and ``c`` have the most words.

Example: file types
-------------------

Work out the relative distribution of file extensions in a source tree::

    ack -f | fgrep . | awk -F . '{print $NF}' | anytop

.. image:: http://media.quietlyamused.org.s3.amazonaws.com/anytop/img/anytop-sourcetree.png

Looks like a PHP codebase for a web app.

Example: shell commands
-----------------------

See what commands you use most often in bash::

    cut -d ' ' -f 1 .bash_history | xargs -n 1 basename | anytop

.. image:: http://media.quietlyamused.org.s3.amazonaws.com/anytop/img/anytop-bashhist.png

Developer tools ``vim``, ``git`` and ``j`` (autojump) feature pretty prominently.  Maybe I type ``ls`` a little too much.

As you can see, ``anytop`` lends itself handily to shell pipelines, allowing
it to be useful in a wide variety of situations.

Memory usage
------------

Anytop uses memory proportional to the number of distinct lines in the input.
If the input keyspace is bounded, then anytop will use limited memory, no
matter how many lines or how long it runs.

When the input keyspace is not bounded, memory use can still be bounded by
only displaying statistics on a fixed-size window of lines with the ``-l``
option.

