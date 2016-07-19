from setuptools import setup

setup(
    name="PyJSONAPIClient",
    version="0.1",
    install_requires=[
        "requests"
    ],
    tests_require=[
        "mock",
        "nose2"
    ]
)
