import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '0.0.4'

README = read('README.rst')
CHANGES = read('CHANGES.rst')

setup(
    name="pipfreeze",
    version=version,
    author="Alex Conrad",
    author_email="alexandre@surveymonkey.com",
    maintainer="Alex Conrad",
    maintainer_email="alexandre@surveymonkey.com",
    description="A tool to audit pip freeze outputs "
                "and test version requirements",
    license="MIT License",
    keywords="pip freeze output audit version requirements satified",
    url="https://github.com/SurveyMonkey/pipfreeze",
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
    long_description='%s\n\n%s' % (README, CHANGES),
    setup_requires=['setuptools_git'],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ],
)
