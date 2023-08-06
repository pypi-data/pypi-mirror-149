from setuptools import setup, find_packages

setup(
    name='cid-client',
    version='0.1.5',
    license='MIT',
    description='Client of CID Tool',
    url='https://github.com/coherentdigital/cid-python',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'requests'
    ]
)
