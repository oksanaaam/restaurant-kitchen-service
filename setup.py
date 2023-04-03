from setuptools import setup, find_packages

setup(
    name='restaurant',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'django',
        'psycopg2-binary',
    ],
)
