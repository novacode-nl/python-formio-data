from setuptools import setup, find_packages

# TODO
# packages = find_packages(exclude=['tests*'])

setup(
    name='python-formio-data',
    version='0.1.0.dev1',
    description='Python object API for Form.io (JSON) data',
    url='https://github.com/novacode-nl/python-formio-data',
    author='Bob Leers',
    author_email='bob@novacode.nl',
    license='MIT',
    packages=[
        'formio_data'
    ],
    # install_requires=[]
)
