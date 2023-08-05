from setuptools import setup, find_packages
from pathlib import Path

path = Path(__file__).resolve().parent
with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()


setup(name='networktools',
      version=version,
      description='NetworkTools are some special functions to help with software developing',
      url='http://www.gitlab.com/dpineda/networktools',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPL3',
      install_requires=[
          "termcolor",
          "pytz", 
          "ujson", 
          'validators', 
          "dataclasses-json", 
          "boltons"],
      packages=find_packages(),
      include_package_data=True,      
      package_dir={'networktools': 'networktools'},
      package_data={
          'networktools': ['../doc', '../docs', '../requeriments.txt']},
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
