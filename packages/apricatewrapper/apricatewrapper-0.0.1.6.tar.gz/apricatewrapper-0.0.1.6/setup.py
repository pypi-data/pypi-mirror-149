from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r") as req_file:
    requirements = req_file.read()

setup(
    name="apricatewrapper",
    version="0.0.1.6",
    author="Mads Jensen",
    author_email="",
    description="A wrapper around the Apricate.io API in python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Denmads/ApricateIO-Wrapper",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)