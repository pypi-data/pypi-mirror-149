from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tendermintwallet',
    version='0.0.2',
    packages=['tendermintwallet', 'tendermintwallet.interfaces'],
    url='https://github.com/algo-vaultstaking/tendermintwallet',
    license='MIT',
    author='AlgoRhythm',
    author_email='',
    description='Tools for tendermint-based wallet management, offline transaction signing and broadcasting',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'ecdsa',
        'bech32',
        'hdwallets',
        'mnemonic',
        'typing-extensions',
        'requests',
        'google',
        'protobuf'
      ],
    zip_safe=False,
)
