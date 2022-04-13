#!/usr/bin/env python

from distutils.core import setup
from os.path import join, dirname
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

requirementstxt = join(dirname(__file__), "requirements.txt")
requirements = [line.strip() for line in open(requirementstxt, "r") if line.strip()]

scripts = glob.glob('alignment/*.py')
scripts += glob.glob('data_preparation/*.py')
scripts += glob.glob('interfaces/*.py')
scripts += glob.glob('pipelines/*.py')
scripts += glob.glob('pipelines/*.sh')

setup(name='finnish_forced_alignment',
      version=0,
      description='finnish forced alignment',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Juho Leinonen',
      author_email='juho.leinonen@aalto.fi',
      url='https://github.com/aalto-speech/finnish-forced-alignment',
      packages=['finnish_forced_alignment'],
      package_data={'finnish_forced_alignment': ['g2p_mappings/*.csv']},
      include_package_data=True,
      scripts=scripts,
      python_requires=">=3.6",
      install_requires=requirements,
      classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Speech Recognition",
      ],
      )

