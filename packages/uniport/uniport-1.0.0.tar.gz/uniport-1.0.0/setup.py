from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = "uniport",
    version = "1.0.0",
    description = "a unified computational framework for single-cell data integration with optimal transport",
    python_requires=">3.6.0",
    install_requires=requirements,
    license = "MIT Licence",

    url = "https://github.com/caokai1073/uniPort",
    author = "caokai",
    author_email = "caokai@amss.ac.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
)
