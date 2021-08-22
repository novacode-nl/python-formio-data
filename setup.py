from setuptools import setup, find_packages

packages = find_packages(exclude=['tests*'])

setup(
    name='formio-data',
    version='0.3.14',
    description='formio.js JSON-data API',
    url='https://github.com/novacode-nl/python-formio-data',
    author='Bob Leers',
    author_email='bob@novacode.nl',
    license='MIT',
    packages=packages,
    extras_require={
        # Optional dependencies
        'json_logic': ['json-logic-qubit'],
    },
 )
