KiWIS Example
=============

Accessing KiWIS data
--------------------

This example demonstrates how to access and plot time series data from KiWIS
using Python.

.. plot:: scripts/kiwis-example.py
   :include-source:

Writing data to KiWIS
---------------------

Currently KiWIS doesn't allow to write data into or create time series. However,
you can use the :doc:`../stores/file_store` module to save your data locally.

For example, this code snippet continues from the example above and writes the
time series variable ``ts`` to a ZRX file using the ZRXPFormat.

.. code-block:: python

    from kisters.water.time_series.file_io import ZRXPFormat
    writer = ZRXPFormat().writer()
    writer.write('my_time_series.zrx', [ts])
