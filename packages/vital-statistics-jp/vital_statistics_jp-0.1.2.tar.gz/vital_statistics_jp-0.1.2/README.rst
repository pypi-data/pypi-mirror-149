===================
vital_statistics_jp
===================

description
============

This module gets the vital statistics of Japan. Currently, it is possible to obtain monthly prompt data.

install
========

.. code-block:: shell

    pip install vital_statistics_jp

code example
============

.. code-block:: python

    from vital_statistics_jp import read_prompt

    stat_df = read_prompt()

    print(stat_df)

