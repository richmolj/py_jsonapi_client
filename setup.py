from setuptools import setup

setup(
    name="PyJSONAPIClient",
    version="0.1",
    install_requires=[
        "requests",
        "inflection"
    ],
    tests_require=[
        "mock",
        "nose2"
    ]
)
