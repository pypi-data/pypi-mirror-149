from setuptools import setup, Extension
import os

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pegasus_client',
    packages=['pegasus_client', 'pegasus_client.routes',
              'pegasus_client.default_modules', 'pegasus_client.default_modules.generic'],
    version='0.11',
    license='MIT',
    description='Command-line and web tool with modular interface.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Euan Campbell',
    author_email='dev@euan.app',
    url='https://github.com/euanacampbell/pegasus',
    download_url='https://github.com/euanacampbell/pegasus/archive/refs/heads/master.tar.gz',
    keywords=['command-line', 'web', 'tool'],
    include_package_data=True,
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
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
