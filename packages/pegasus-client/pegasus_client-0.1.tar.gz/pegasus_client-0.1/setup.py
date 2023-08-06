from setuptools import setup, Extension
import os

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # How you named your package folder (MyLib)
    name='pegasus_client',
    packages=['pegasus_client'],   # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    license='MIT',
    # Give a short description about your library
    description='Command-line and web tool with modular interface.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Euan Campbell',                   # Type in your name
    author_email='dev@euan.app',
    # Provide either the link to your github or to your website
    url='https://github.com/euanacampbell/pegasus',
    # I explain this later on
    download_url='https://github.com/euanacampbell/pegasus/archive/refs/heads/master.tar.gz',
    # Keywords that define your package best
    keywords=['command-line', 'web', 'tool'],
    install_requires=[
        'requests',
        'pylint',
        'PyMySQL',
        'pyperclip',
        'sqlparse',
        'rich',
        'requests',
        'psutil',
        'gunicorn',
        'PyYAML',
        'flask',
        'pyodbc',
        'tabulate'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Specify which python versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
