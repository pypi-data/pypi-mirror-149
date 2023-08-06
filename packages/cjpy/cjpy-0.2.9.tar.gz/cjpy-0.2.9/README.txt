Usage: cjpy  json_input_file1 -options_for_file1 ... \
            [json_input_file2 -options_for_file2 ...] \
            [--with common_json_files -common_options ...]

Command liner for python routines using json based input parameter files.
Ver 0.2.9 by Jaesub Hong (jhong@cfa.harvard.edu)

      cjpy --help [overview json pars cmdline all ... func:]
      cjpy [json_files ...] --Help
      cjpy --main module.routine --Help

## Installation and Startup

Install the cjpy package using pip,

      % pip install cjpy

then assign an alias for easy use: e.g., in bash,

      % alias cjpy="python -m cjpy"

Alternatively, this program can be used without installation: simply
place cjson.py in the python path and use

      % alias cjpy="python cjson.py"

For a common parameter configuration, assign an environmental variable
CJSON_STARTUP to a JSON file with the common paramters: e.g.,
in bash,

      % export CJSON_STARTUP="~/my_startup.json"

The parameters in this file will be loaded as well.

By default, cjpy will attempt to pass parameters starting only with alphabets
to the routine in call, but one can accept the full parameter sets
(including -main) by adding an optional parameter in your function:

      import cjpy.cjson
      ...
      def my_routine(..., cfg=cjson.native, ...):
            ...

then, cfg, which is an collections.OrderedDict, will
inherit all the parameters.

One can also use cjpy inside python or ipython for a single task: e.g.,

      >>> import cjpy.cjson as cj
      >>> cfg = cj.get_parameters(['json file name','options', ...])
      >>> out = cj.execute(cfg)

Or the args contain a set of parameters for multiple tasks:

      >>> sets=cj.get_parameter_sets(['input args string array'])
      >>> out=cj.execute_sets(sets)


## Quick Overview of the Basic Concept:

The cjson input parameter files can contain the name of the routine to call:
e.g., "-main": "module.routine".  Keys starting with alphabets are assumed to be
fed into the main routine set by "-main" key.  Assume that a python script
example.py has

      def my_sum(name, x, y):
           """ This is my sum. """
           print(name+':', x+y)

Then with a json file input.json,

      "-main": "example.my_sum",
          "x": 5,
          "y": 7,
       "name": "answer",

one can execute the routine my_sum in a shell command prompt like

      % cjpy input.json
      answer: 12

In princinple, all the content in the json files can be fed as a long string in
the command line or as optional parameters for individual keys with "-". So the
above example is equivalent to the followings even without the json file
input.json.

      % cjpy --main example.my_sum -#x 5 -#y 7 -name "answer"
      % cjpy '{"-main":"example.my_sum","x":5,"y":7,"name":"answer"}'

or some combination of all three examples:

      % cjpy '{"-main":"example.my_sum","name":"answer"}' -#x 5 -#y 7
      % cjpy input.json '{"name":"answer"}' -#x 5 -#y 7

When both json files and command line input options are available for the same
key, the command line options take a priority.  Note # in -#x ensures it is a
number but not a string.  See more details with cjpy --help cmdline. Note --Help
(capital H) prints out the doc string of the routine.

      % cjpy input.json --Help
      This is my sum.

Calling multiple JSON files execute them in sequence.

      % cjpy input.json input.json
      answer: 12
      answer: 12

      % cjpy input.json -#x 7 input.json -#x 6
      answer: 14
      answer: 13

Find out what kind of parameters are needed to call the routine using --show
func option.

      % cjpy --main os.path.isfile --show func
       main: os.path.isfile
       path

The above example shows isfile expect a parameter called path.

      % cjpy --main os.path.isfile -path cjson.py --show output
      True

Can check how the parameters get fed to the routine.

      % cjpy --main os.path.isfile -path cjson.py --show feed
       main: os.path.isfile
       path << str cjson.py

      % cjpy input.json --show feed
       main: example.my_sum
       name << str answer
          x << int 5
          y << int 7

Can call a routine needing no input parameters.

      % cjpy --main datetime.datetime.now --show output
      2022-04-27 22:11:52.983532

One can force the parameters to a function with --pars option.

      % cjpy --main math.sin --pars x --show output -#x 1.0
      0.8414709848078965

In the case of the built-in functions: e.g.,

      % cjpy --main eval --pars x --show output -x 3+3
      6

      % cjpy --main pow -*-pars x,y --show output -#x 1.5 -#y 3
      3.375

      % cjpy --main eval --pars x --show output -x 'pow(1.5,3)'
      3.375


try also:
       --help overview | features | json | pars | startup | iteration |
             decoration | logging | sequential | cmdline | changes | all | func:
             | func:[function name]
