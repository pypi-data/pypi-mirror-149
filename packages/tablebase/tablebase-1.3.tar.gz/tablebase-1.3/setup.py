from setuptools import setup, find_packages

setup(
    name='tablebase',
    version='1.3',
    description='To make tables in python as easy as printing to the console',
    author='Maximilian Lange',
    author_email='maxhlange@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
