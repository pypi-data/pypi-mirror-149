===================
vital_statistics_jp
===================

description
============

This module gets the vital statistics of Japan. Currently, it is possible to obtain monthly prompt data.

install
========

.. code-block:: shell

    pip install vital-statistics-jp

code example
============

.. code-block:: python

    from vital-statistics-jp import read_prompt

    stat_df = read_prompt()

    print(stat_df)

