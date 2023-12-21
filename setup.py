from setuptools import setup
from setuptools import find_packages

setup(
    name='verimedian',
    version='0.1.0',
    packages=find_packages(include=['verimedian']),
    package_data={'': ['poseidon_constants_opt.json']},
    include_package_data=True,
)
