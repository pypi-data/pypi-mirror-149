import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="orwell_translators",
    version="1.1.4",
    description="Create translators for the Orwell platform",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://orwellmonitoring.github.io/",
    author="Orwell",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["orwell"],
    include_package_data=True,
    install_requires=["flask", "kafka-python", "redis"]
)