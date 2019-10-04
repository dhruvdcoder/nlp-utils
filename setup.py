from setuptools import setup, find_packages
from pathlib import Path

requirements_file = Path('requirements.txt')

if (not requirements_file.exists()) or (not requirements_file.is_file()):
    raise Exception("No requirements.txt found")
with open(requirements_file) as f:
    install_requires = list(f.read().splitlines())

setup(
    name='nlp_utils',
    version='0.0.1',
    description='Utilites for NLP',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={'nlp_utils': ['py.typed']},
    install_requires=install_requires,
    zip_safe=False)
