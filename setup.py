#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(name = 'org-voice-notes',
      version = "1.0.1",
      description = "A tool to convert voice notes to an Org file.",
      long_descrniption = long_description,
      long_description_content_type = "text/markdown",
      author = "Samuel W. Flint",
      author_email = "swflint@flintfam.org",
      license="GPL3+",
      url="https://github.com/swflint/org-voice-notes",
      packages=find_packages(where = "src"),
      package_dir={"": "src"},
      scripts=['bin/org-voice-notes'],
      install_requires=["requests",
                        "jsonpickle",
                        "tqdm"])
