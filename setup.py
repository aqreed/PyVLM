from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vlm",
    author='aqreed',
    description='Python Vortex Lattice Method',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.0.1",
    url='https://github.com/aqreed/PyVLM',
    packages=['vlm'],
    install_requires=['numpy', 'matplotlib'],
    tests_requires=['pytest']
    )
