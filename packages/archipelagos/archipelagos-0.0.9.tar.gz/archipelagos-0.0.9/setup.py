import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="archipelagos",
    version="0.0.9",
    description="The Python Client for the Archipelagos platform.",

    long_description=README,
    long_description_content_type="text/markdown",

    url="https://www.archipelagos-labs.com",
    license="Apache License, Version 2.0",

    author="Archipelagos Labs",
    author_email="support@archipelagos-labs.com",

    classifiers=["Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10"],

    packages=["archipelagos",
              "archipelagos.common",
              "archipelagos.common.data",
              "archipelagos.common.protobuf",
              "archipelagos.common.protobuf.common",
              "archipelagos.common.protobuf.common.user",
              "archipelagos.common.protobuf.common.data",
              "archipelagos.common.protobuf.common.data.collection",
              "archipelagos.common.protobuf.common.data.filestore",
              "archipelagos.common.protobuf.common.data.timeseries"],
    include_package_data=True,

    install_requires=["numpy>=1.21.2",
                      "pandas>=1.3.5",
                      "protobuf>=3.19.1",
                      "requests>=2.27.1"],

    extras_require={"all": ["geopandas>=0.10.2"]}
)
