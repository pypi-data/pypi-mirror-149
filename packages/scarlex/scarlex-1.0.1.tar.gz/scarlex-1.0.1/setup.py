from setuptools import setup

description = """
Scarlex API Wrapper
-------------------
A simple api wrapper for Scarlex.
"""

setup(
    name='scarlex',
    version='1.0.1',
    author='avixity',
    description=description,
    license='MIT',
    keywords=['scarlex', 'api'],
    install_requires=['aiohttp'],
    packages=["scarlex"]
)
