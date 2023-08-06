#!/usr/bin/env python
import os
from distutils.command.sdist import sdist as sdist_orig
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

    def find_packages(where='.'):
        # os.walk -> list[(dirname, list[subdirs], list[files])]
        return [folder.replace(os.sep, ".").strip(".")
                for (folder, _, files) in os.walk(where)
                if "__init__.py" in files]


class MyInstall(sdist_orig):
    def run(self):
        super().run()


setup(
    name='transgit',
    version='0.0.1',
    url='https://pedrohavay.com',
    description='Open source tool to export Gitlab repositories to Github.',
    keywords='Git,Github,Gitlab',
    author='Pedro Havay',
    author_email='admin@pedrohavay.com',
    maintainer='Pedro Havay',
    platforms=['any'],
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    cmdclass={
        'run': MyInstall
    },
    entry_points={
        "console_scripts": [
            "transgit = transgit.cli:main",
        ]
    },
    install_requires=[
        "click",
        "colorama",
    ],
    extras_require={
        'complete': [
            # 'pyOpenSSL'
        ],
    }
)
