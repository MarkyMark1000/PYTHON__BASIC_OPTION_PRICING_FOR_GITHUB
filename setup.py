from setuptools import find_packages, setup

setup(
    name='BasicOptionPricing',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'matplotlib',
    ],
    author="Mark Wilson",
    author_email="mark_john_wilson@yahoo.co.uk",
    description="Investigate numpy etc with basic option pricing",
    long_description=open('README.txt').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/.....",
    license='Creative Commons Attribution-Noncommercial-Share Alike license'
    )