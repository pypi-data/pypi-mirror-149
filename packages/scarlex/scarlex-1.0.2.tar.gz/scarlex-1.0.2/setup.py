import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()
description = """
Scarlex API Wrapper
-------------------
A simple api wrapper for Scarlex.
"""

setuptools.setup(
    name='scarlex',
    version='1.0.2',
    author='avixity',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScarlexDev/ScarlexPY",
    license='Apache 2.0',
    keywords=['scarlex', 'api'],
    install_requires=['aiohttp'],
    packages=["scarlex"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
