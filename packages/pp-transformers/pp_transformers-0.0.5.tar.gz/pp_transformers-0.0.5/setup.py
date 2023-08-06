
from setuptools import setup, find_packages

setup(
    name="pp_transformers",
    version="0.0.5",
    description="transformer of paddle",
    long_description="time and path tool",
    license="MIT Licence",
    author="bei",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "paddlenlp>=2.2.5",
        "transformers"
    ]
)