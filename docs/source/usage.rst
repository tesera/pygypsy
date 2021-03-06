Data Management
===============

Output for each pygypsy command is created at a fixed path relative to a
configurable output directory

The output directory can be specified after the pygypsy command and before
subcommands, e.g.

::

   pygypsy --output-dir /your/own/output-dir generate_config

This way you can manage data for several simulations

::

   pygypsy --output-dir /lothlorien simulate /lothlorien/plot_data_prepped.csv
   pygypsy --output-dir /mirkwood simulate /mirkwood/plot_data_prepped.csv
   pygypsy --output-dir /mirkwood-5-year simulate /mirkwood-5-year/plot_data_prepped.csv

If it is not specified, the default output directory, ``./pygypsy-output`` will
be used.

Configuration
=============

A configuration file is needed to run the gypsy simulation

A template configuration can be generated as follows:

::

    pygypsy generate_config

The configuration file is a json file and must follow `json syntax <http://www.w3schools.com/js/js_json_syntax.asp>`__.

It is generally safe to replace values in the configuration files with new
values of the same type (e.g. replace integers with integers).

The schema, against which the configuration file is validated, is available
`here
<https://github.com/tesera/pygypsy/blob/dev/pygypsy/scripts/config/conf.schema>`__.

Growing Plots
-------------

To bring plot data to the current date, and combination of configuration files
parameters can be used:

E.g. to bring data collected in 2011 to date as of 2017 use the following
values in the configuration file: ::

    {
        # other variables ...
        "simulation": {
            "years": 6,
            "backwards": false
        },
        "data": {
            "acquistionYear": 2011
        },
        "output": {
            "level": "annual"
        },
        # other variables ...
    }

The output will be a file for each year, with each file containing the
properties of all the plots.

Developing Yield Curves
-----------------------

Yield curve development is another common use case, this consists, for example,
of plot-level simulations of 250 year duration. The following configuration
values will produce one output file for each plot, with the gypsy properties
for each year of the simulation: ::


    {
        # other variables ...
        "simulation": {
            "years": 250,
            "backwards": true
        },
        "data": {
            "acquistionYear": 0
        },
        "output": {
            "level": "plot"
        },
        # other variables ...
    }

Backwards simulation
--------------------

The backwards configuration: ::

    {
        # other variables ...
        "simulation": {
            # other variables ...
            "backwards": true
    },

Controls whether the curve is simulated from primary succession. If true, the
simulation goes from a clear plot until the simulation duration. If false, the
simulation goes from the time of data acquisition until the simulation duration.

Simulations
===========

With the output directory and configuration file prepared, the next steps are
to:

- prepare the plot data for use with pygypsy
- run the simulation on the prepared plot data


Preparing plot data
-------------------

Prepare your plot data as follows

::

   pygypsy prep --config-file ./pygypsy-output/pygypsy-config.json /path/to/your/plot-data.csv

Take note of the console output to see where the prepared plot data is created.

Running simulation
------------------

Run the gypsy simulation as follows

::

   pygypsy simulate --config-file ./pygypsy-output/config.json /pygypsy-output/plot_data_prepped.csv

Troubleshooting
===============

If you run into issues with pygypsy, there are a few things to check and
record:

- the messages output in the terminal
- the logs for each subcommand, which are saved under the output directory

If you cannot resolve the issue based on information in those resources, open a
|new pygypsy issue|, including the messages output by the CLI in the terminal,
and the log files in the corresponding output directory.

.. |new pygypsy issue| replace:: `new pygypsy issue <https://github.com/tesera/pygypsy/issues/new>`__
