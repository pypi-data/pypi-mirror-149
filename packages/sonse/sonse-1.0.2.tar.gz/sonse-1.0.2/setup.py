"""
PyPi setup script.
"""

from setuptools import find_packages, setup

from sonse import VERSION_NUMBER

# fmt: off

setup(
    # Basic information.
    name         = "sonse",
    version      = VERSION_NUMBER,
    keywords     = "notes note-taking cli",
    description  = "Stephen's Obsessive Note-Storage Engine.",
    url          = "https://github.com/rattlerake/sonse",
    author       = "Stephen Malone",
    author_email = "mail@sonse.org",

    # Project description.
    long_description = open("readme.md").read(),
    long_description_content_type = "text/markdown",

    # Package specifications.
    packages = find_packages(exclude=["*tests*"]),
    python_requires  = ">=3.10",
    install_requires = ["click>=8.1"],

    # Console executables.
    entry_points = {
        "console_scripts": ["sonse=sonse.__main__:group.main"],
    },

    # Project URLs.
    project_urls = {
        "Changelog": "https://github.com/rattlerake/sonse/blob/main/changes.md",
        "Issues":    "https://github.com/rattlerake/sonse/issues",
    },

    # Project classifiers.
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
)
