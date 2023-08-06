from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Repometrics_CLI',
    version='0.0.4',
    packages=find_packages(),
    url='https://github.com/Edward1101/Repometrics_CLI',
    license='MIT',
    author='Edward Li Shuyao',
    author_email='lishuyao1101@hotmail.com',
    description='CLI to display repository files programing languages.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pygments'],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'Repometrics_CLI = Repometrics_CLI.Repometrics_CLI:main'
        ]
    }
)
