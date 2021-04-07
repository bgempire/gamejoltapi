#!/usr/bin/env python
from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(name="gamejoltapi",
      version="0.0.1",
      author="Joel Gomes da Silva",
      author_email="joelgomes1994@hotmail.com",
      description="Single threaded Python interface for the GameJolt API running through HTTP requests",
      license="MIT",
      keywords="game gamedev api interface gamejolt gamejoltapi",
      url="https://github.com/bgempire/gamejoltapi",
      long_description_content_type = "text/markdown",
      long_description=readme,
      py_modules=['gamejoltapi'],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3 :: Only",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development :: Libraries"])
