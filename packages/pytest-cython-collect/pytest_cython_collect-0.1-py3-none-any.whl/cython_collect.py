import importlib
import os
import pathlib
import sysconfig

import pytest
from pytest import Function

EXT_SUFFIX = sysconfig.get_config_var("EXT_SUFFIX")

# NOTE: This file contains modified code from pytest-cython:
# https://github.com/lgpage/pytest-cython/blob/master/src/pytest_cython/plugin.py

def pytest_addoption(parser):
    group = parser.getgroup("cython")
    group.addoption(
        "--cython-collect",
        action="store_true",
        default=False,
        help="Collect tests from cython-compiled .py or .pyx files",
        dest="cython_collect",
    )


def pytest_collect_file(path, parent):
    if not parent.config.getoption("--cython-collect"):
        return

    cy_exts = [".py", ".pxd", ".pyx"]

    if (
        path.ext in cy_exts and path.new(ext=EXT_SUFFIX).check()
    ):  # Verify extension, and that it has been compiled
        if hasattr(CythonModule, "from_parent"):
            return CythonModule.from_parent(parent, path=pathlib.Path(path))
        else:
            # Backwards-compat for older pytest
            return CythonModule(path, parent)


class CythonModule(pytest.Module):
    def collect(self):
        mod = importlib.import_module(
            os.path.splitext(os.path.basename(self.fspath))[0]
        )
        # test_classes = [x for x in dir(mod) if x.startswith("Test")]

        def yield_functions(mod_class):
            for test_name in (x for x in dir(mod_class) if x.startswith("test_")):
                _test_fn = getattr(mod_class, test_name)
                if callable(_test_fn):
                    # if 'class' in str(mod_class):
                    #     fn = partial(_test_fn, mod_class) # NOTE: Doesn't work
                    #     yield Function.from_parent(self, name=test_name, callobj=fn)
                    yield Function.from_parent(self, name=test_name, callobj=_test_fn)

        yield from yield_functions(mod)

        # for _class in test_classes:
        #     yield from yield_functions(getattr(mod, _class))
