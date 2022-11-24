"""
Set up
"""
from setuptools import setup, find_packages
"""
This MUST match the repo name
If the repo name has dashes name
here should use underscores
"""
__version__ = None
name = 'rulefinder'
exec(open(f"{name}/_version.py").read())
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(name=name, version=__version__,
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements,
      entry_points={
        'console_scripts': [
            'rulefinder = rulefinder.app:main',
            'rulefinder.dbupdate = rulefinder.dbupdate:recreate_table'
		    ],
        },
    )