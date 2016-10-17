from setuptools import setup, find_packages

setup(
    name="PyVLM",
    version="0.0.dev0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['numpy', 'matplotlib'],
    tests_requires=['pytest']
    )