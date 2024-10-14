Debug on level pytest
=====================

These aspects makes it difficult to debug pytest:

* pytest is a highly generic framework. Understanding the traceback is very difficult.
* Very long tracebacks: Similar to java programs, the traceback may get extremly long.
* pytest captures stdout/stderr. The output will be stored and displayed only if an error occured in the error summary.

Best practices for debugging
-----------------------------

* Use the `pytest -s` flag. This will instruct pytest do NOT capture output.
* Limit problem to one test using `pyest testfile.py::test_func[params]`.
* No use the VSCode debugger to investigate further. See details below.

Debug pytest using the VSCode debugger
--------------------------------------

Start with this VSCode workspace: `<repo>/testbed_tutorial.code-workspace`

Use the VSCode pytest test explorer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: images/pytest_test_explorer.png
    :align: center

The setup is a bit tricky! These config parameters have to be set correctly:

`testbed_tutorial.code-workspace`:

.. code-block:: json

	"settings": {
		"python.testing.pytestArgs": [
			// "--firmware-json=${workspaceFolder}/pytest_args_firmware_RPI_PICO_v1.23.0.json",
			"--firmware-json=${workspaceFolder}/pytest_args_firmware_RPI_PICO2_v1.24.0.json",
			"tests"
		],
		"python.testing.cwd": "${workspaceFolder}",
		"python.testing.unittestEnabled": false,
		"python.testing.pytestEnabled": true
	},

`python.testing.pytestArgs` has an influence of the test selection in the pytest explorer!

Use the VSCode debugger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the easiest way to debug!

I assume, that you may run the pytest command line.

Now lets run the exactly same command in the VSCode debugger.

`.vscode/launch.json`:

.. code-block:: json

    "configurations": [
        {
            "name": "pytest RPI_PICO 1.23.0 - test_github_micropython_org --collect-only --firmware-json",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "cwd": "${workspaceFolder}",
            "args": [
                "--collect-only",
                "-q",
                "--git-micropython=https://github.com/micropython/micropython.git@master",
                "--firmware-json=${workspaceFolder}/pytest_args_firmware_RPI_PICO_v1.23.0.json",
                "tests/tests_github_micropython_org/test_github_micropython_org.py"
            ],
            "console": "integratedTerminal",
            "env": {
                "PYDEVD_DISABLE_FILE_VALIDATION": "1"
            },
            "justMyCode": false,
        },

Please adapt `args` to reflect your command line arguments!

Note that `"module": "pytest"` indicates VSCode to start this command in the debugger: `python -m pytest`!



pytest will NOT enter the debugger, however, VSCode should
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

pytest will catch all exception and collect the results. However, during debugging, we want VSCode to stop on the first exception!

The following code implements this functionality and is activated automatically in `tests/conftest.py` !

.. automethod:: octoprobe.util_pytest.util_vscode::break_into_debugger_on_exception()
    :no-index: