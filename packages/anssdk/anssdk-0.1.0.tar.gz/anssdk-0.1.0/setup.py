from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'Python SDK to resolve ANS .algo names'
LONG_DESCRIPTION = 'This Python SDK helps in resolving ANS .algo names to wallet addresses and view names owned by a specific Algorand Wallet address'

# Setting up
setup(
    name="anssdk",
    version=VERSION,
    author="Algorand Name Service",
    author_email="contact@algonameservice.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'algorand', 'algorand name service', 'py-sdk', 'name service', '.algo'],
    
)