import codecs
import os.path
from setuptools import setup, find_packages
# from Perceived_safety_choice_model import _version_

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

description = """
The model that has been uploaded to this repository aspires to describe routing behavior 
of micro-mobility modes, e.g., e-bikes and e-scoters, in relationship with traditional modes, 
e.g., private car and walking.
"""
setup(name = "psafechoices",
      version = get_version("psafechoices/__init__.py"),
      url = "https://github.com/panosgjuras/Perceived_safety_choices",
      author = "Panagiotis G. Tzouras",
      author_email = "ptzouras@mail.ntua.gr",
      description=" ".join(description.strip().splitlines()),
      packages = ["psafechoices"]
      )