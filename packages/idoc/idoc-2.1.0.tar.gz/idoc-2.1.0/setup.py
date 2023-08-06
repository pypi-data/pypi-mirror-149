import os.path
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install


with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION="2.1.0"
PKG_NAME="idoc"
with open(os.path.join(PKG_NAME, "__init__.py"), "w") as filehandle:
    filehandle.write(f"__version__=\"{VERSION}\"\n")


setup(
    name=PKG_NAME,
    version=VERSION,
    author="Antonio Ortega",
    author_email="antonio.ortega@kuleuven.be",
    description="Individual Drosophila Optogenetics Conditioner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shaliulab/idoc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    include_package_data=True,
    install_requires = [
        "pypylon",
        "opencv-python>=4.1.1",
        "pyserial>=3.4",
        "scipy",
        "numpy",
        "pandas",
        "pyfirmata",
        "pyaml",
        "coloredlogs",
        "bottle",
        "cheroot",
        "netifaces",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "idoc_server=idoc.server.bin.server:main",
            "idoc_client=idoc.client.bin.client:main",
            "idoc_cli=idoc.client.bin.cli:main",
            "idoc_offline=idoc.server.bin.offline:offline",
            "idoc_config=idoc.configuration:integrity_check",
        ]
    },
    python_requires='>=3.8.10',
)
