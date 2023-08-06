# Pytest Cython Collect

Very simple Pytest plugin, which searches for `.pyx` files and methods inside the compiled `.so` files to collect tests.

To use the plugin, add the `--cython-collect` option when calling `pytest`.


There are currently several limitations:

 * Fixtures defined inside the cython-compiled code will not be registered by Pytest.
    - Fixtures defined in `.py` files, which are not compiled, can be used.
 * Pytest decorators are generally not supported yet (`@pytest.mark.parametrize...`)
    - This could possibly be fixed by adding a new decorator or some more logic when collecting
 * Test classes are not collected
 * `.pyx` and `.py` files are not automatically cythonized. You'll need to build them yourself first


# Acknowledgements

This plugin contains code from [pytest-cython](https://github.com/lgpage/pytest-cython).


