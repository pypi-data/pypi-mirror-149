import os

from setuptools import setup

version = os.getenv("GITHUB_REF", "refs/tags/v0.0.0").split("/")[-1]
print(f"Building version: {version}")

setup(
    name="pytest-cython-collect",
    classifiers=["Framework :: Pytest"],
    version=version,
    author="Mads Ynddal",
    author_email="mads@ynddal.dk",
    url="https://github.com/Baekalfen/pytest-cython-collect",
    py_modules=["cython_collect"],
    install_requires=[
        'pytest',
    ],
    entry_points={
        'pytest11': [
            'pytest_cython_collect = cython_collect',
        ],
    },
)
