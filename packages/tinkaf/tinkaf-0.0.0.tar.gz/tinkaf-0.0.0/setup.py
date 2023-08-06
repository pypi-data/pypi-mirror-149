import os
from glob import glob

from setuptools import find_packages, setup

from tinkaf import __name__, __version__

requirements = {}
for path in glob("requirements/*.txt"):
    with open(path) as file:
        name = os.path.basename(path)[:-4]
        requirements[name] = [line.strip() for line in file]

with open("README.md") as file:
    long_description = file.read()

github_link = "https://github.com/0dminnimda/Tinkoff-Algotrading-Framework"

setup(
    name=__name__,
    version=__version__,
    description="TINKoff Algotrading Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="0dminnimda",
    author_email="0dminnimda.contact@gmail.com",
    url=github_link,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    license="Apache-2.0",
    project_urls={
        "Bug tracker": github_link + "/issues",
    },
    install_requires=requirements.pop("basic"),
    python_requires=">=3.8",
    extras_require=requirements,
)
