from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vlmpy",
    author='aqreed',
    description='Python Vortex Lattice Method',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.0.1",
    url='https://github.com/aqreed/vlmpy',
    packages=['vlmpy'],
    install_requires=['numpy', 'matplotlib'],
    tests_requires=['pytest']
    )
