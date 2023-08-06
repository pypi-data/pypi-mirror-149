from setuptools import setup, find_packages
import io
from os import path
requirements = [l.strip() for l in open('requirements.txt').readlines()]

# requirements = ['streamlit==0.78.0','geopy==1.20.0','geographiclib==1.50','mysql-connector==2.2.9','click==7.1.2','pandas==1.1.5','plotly==5.3.1','kaleido==0.2.1']
requirements = [l for l in requirements if not l.startswith('streamlit')]

# Get the long description from the README file

here = path.abspath(path.dirname(__file__))

with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='liveisstracker',
    url='https://gitlab.com/manojm18',
    version='1.1.0',
    author='Manoj Manivannan',
    author_email='manojm18@live.in',
    description='A CLI based on the LiveIssTracker Project from https://gitlab.com/manojm18/liveisstracker',
    long_description=long_description,
    packages=find_packages(),
    entry_points={
    'console_scripts': ['liveisstracker=liveisstracker.command_line:main'],
    },
    install_requires=requirements,
    include_package_data=True,
)

