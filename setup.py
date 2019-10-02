from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vlm",
    author='aqreed',
    description='Python Vortex Lattice Method',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.0.2",
    url='https://github.com/aqreed/PyVLM',
    packages=['vlm'],
    install_requires=['numpy', 'matplotlib'],
    tests_requires=['pytest'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization"
    ]
    )
