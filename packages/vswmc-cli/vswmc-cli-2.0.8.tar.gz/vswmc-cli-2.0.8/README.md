# VSWMC Command-Line Interface

Install with pip:

    pip install --upgrade vswmc-cli

This will install a `vswmc` command on your system. The `vswmc` command has a few global options:

`-u USER`

&nbsp;&nbsp;&nbsp; SSA Username

`-p PASSWORD`

&nbsp;&nbsp;&nbsp; SSA Password


## List available simulations
    vswmc simulations list

This shows the parameters that a run requires.


## Start a run
    vswmc run [--param-file PARAM_FILE] [--param PARAM=VALUE ...] -- SIMULATION

This command returns the ID of the new run via stdout. You can use this ID to fetch the log or fetch result files.

OPTIONS
<dl>
<dt><tt>--param-file PARAM_FILE</tt></dt>
<dd>Read parameters from a file.</dd>
<dt><tt>--param PARAM=VALUE ...</tt></dt>
<dd>Set parameters.</dd>
</dl>

Each simulation supports different parameters. To know what parameters you need for a particular simulation, run:

    vswmc simulations describe SIMULATION


## List runs
    vswmc ps [--simulation SIMULATION] [-a, --all]

OPTIONS
<dl>
<dt><tt>--simulation SIMULATION</tt></dt>
<dd>Filter on simulation.</dd>
<dt><tt>-a, --all</tt></dt>
<dd>List all runs (default shows only ongoing)</dd>
</dl>


## Copy a result file to disk
    vswmc cp SRC DST

Downloads a remote result file to local disk. The source should be specified in the format <tt>RUN:FILE</tt>. The <tt>DST</tt> argument can be a local file or directory.


## Fetch the logs of a run
    vswmc logs RUN


## List the results of a run
    vswmc ls [-l] RUN

OPTIONS
<dl>
<dt><tt>-l</tt></dt>
<dd>Print long listing</dd>
</dl>


## Save all results of a run
    vswmc save RUN

Saves all result files of a run. The results of each individual task in this run are compressed and saved into a zip archive named after the model for that task.


## Stop one or more runs
    vswmc stop RUN ...


## Remove one or more runs
    vswmc rm RUN ...
