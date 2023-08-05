import pathlib
from setuptools import setup, find_packages


def _file_read(path):
    with open(path, 'r') as f:
        return f.read()


def _file_readlines(path):
    with open(path, 'r') as f:
        return f.readlines()


setup(
    name="mycfg",
    version="1.1.9",
    author="pjones123",
    author_email="pjones-uk@outlook.com",
    description="A basic dotfiles manager",
    long_description=_file_read(pathlib.Path("README.md")),
    long_description_content_type="text/markdown",
    url="https://github.com/pjones123/MyCfg",
    packages=find_packages(),
    install_requires=_file_readlines("requirements.txt"),
    include_package_data=True,
    python_requires=">=3.6",
    keywords=["dotfiles"],
    entry_points={"console_scripts": ["mycfg = mycfg.__main__:main"]},
    classifiers=[
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Intended Audience :: End Users/Desktop",
    ],
)
