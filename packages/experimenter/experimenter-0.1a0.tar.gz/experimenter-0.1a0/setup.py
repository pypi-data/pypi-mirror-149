from setuptools import find_packages, setup, Command
from shutil import rmtree
import sys
import os
import io
from pathlib import Path

from os import path
this_directory = os.path.abspath(os.path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


url="https://github.com/facundoq/experimenter"
VERSION="0.1alpha"

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        dist_path=Path(this_directory)/'dist'
        if dist_path.exists():
            self.status('Removing previous builds…')
            rmtree(dist_path)

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


setup(
    name="experimenter",
    version=VERSION,
    python_requires='>=3.6',
    packages=find_packages(),
    scripts=[],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        "texttable",
        "argparse",
        "argcomplete",

    ],

    package_data={

    },
    zip_safe=True,
    # metadata to display on PyPI
    author="Facundo Manuel Quiroga",
    author_email="facundoq@gmail.com",
    description="Lightweight experiment base class, to organize machine learning research projects.",
    keywords="experiment repeatability",
    url=url,   # project home page, if any
    project_urls={
        "Bug Tracker": url+"/issues",
        "Documentation": url,
        "Source Code": url,
    },
    # check list at:
    # https://pypi.org/classifiers/
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        
    ],

    # could also include long_description, download_url, etc.
    long_description=long_description,
    long_description_content_type='text/markdown',
    cmdclass={
        'upload': UploadCommand,
    },
)