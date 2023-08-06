from setuptools import setup, find_packages
from io import open

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pythemer',
    description='A WIP theme engine for macOS, written in Python.',
    version='1.0.1',
    packages=find_packages(),  # list of all packages
    install_requires=['click', 'pyyaml', 'radium'],
    python_requires='>=2.7',  # any python greater than 2.7
    entry_points='''
        [console_scripts]
        themer=themer.__main__:main
    ''',
    author="Jaidan",
    keywords="theme, themes, macos, mac, icon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='JL',
    url='https://github.com/pythemer/themer',
    download_url='https://github.com/pythemer/themer/archive/1.0.0.tar.gz',
    author_email='ajaidan0@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)
