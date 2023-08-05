from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='termx',
    version='0.1.1',
    url='https://github.com/Izaan17/termx',
    packages=find_packages(),
    license='MIT',
    author='Izaan Noman',
    author_email='',
    description='Create terminal applications with ease.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["colorama", "bs4"],
)
