from setuptools import setup

setup(
    name="PyJSONAPIClient",
    version="0.1",
    install_requires=[
        "requests > 2.0, < 3.0",
        "inflection > 0.3, < 0.4"
    ],
    test_suite='nose2.collector.collector',
    tests_require=[
        "mock",
        "nose2"
    ]
)
