#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [x for x in fh.read().splitlines() if x]

setup(name='Mime Codec',
      packages=['mime_codec'],
      version='0.1.1',
      description='get mime codecs for media purposes',
      author='skillor',
      author_email='skillor@gmx.net',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      url='https://github.com/skillor/mime-codec',
      keywords=['mime', 'codec', 'mime-codec', 'mediasource'],
      classifiers=['Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.9',
                   'Topic :: Internet'],
      setup_requires=["wheel"],
      install_requires=requirements,
      include_package_data=True,
      package_data={'': [
          'binaries/ffprobe',
          'binaries/ffprobe.exe',
      ]},
      python_requires='>=3',
      )
