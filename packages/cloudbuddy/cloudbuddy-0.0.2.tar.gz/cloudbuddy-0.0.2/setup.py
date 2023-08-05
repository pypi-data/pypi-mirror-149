from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'AWS Infrastructure automation'
LONG_DESCRIPTION = 'A package that allows to create AWS infra structure with simple config yaml files'
license_file = open("LICENSE.txt")
# Setting up
setup(
    name="cloudbuddy",
    version=VERSION,
    author="Seneca Global",
    author_email="saiphani.alapati@senecaglobal.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['boto3', 'botocore', 'colorama', 'python-dotenv', 'PyYAML', 'pytest'],
    keywords=['python', 'aws', 'automation', 'ecs', 'ecr', 'rds'],
    license=license_file.read(),
    # package_data={"awsinfratool": ["config.yml"]},
    entry_points = {
            'console_scripts': [
                'cloudbuddy = cloudbuddy.main:main'
            ]
        },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
