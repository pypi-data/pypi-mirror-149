from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    readme_md = f.read()


setup(
    name="ech-datastructures",
    version="0.1.3",
    description="Comprehensive package of Python-native datastructures.",
    long_description=readme_md,
    long_description_content_type="text/markdown",
    url="https://github.com/rkechols/ech-datastructures",
    project_urls={
        # "Documentation": "https://packaging.python.org/tutorials/distributing-packages/",
        # "Funding": "https://donate.pypi.org",
        # "Say Thanks!": "http://saythanks.io/to/example",
        # "Source": "https://github.com/pypa/sampleproject/",
        # "Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    author="Ryan Echols",
    author_email="ryan@shadylakemedia.com",
    license="GNU GPL v3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    keywords="data structure structures datastructure datastructures tool tools "
             "util utils utility utilities",
    python_requires=">=3.8",
    packages=find_packages(
        exclude=["tests"]
    ),
    # install_requires=[],
)
