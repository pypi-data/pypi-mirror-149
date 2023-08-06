import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "texta-tools",
    version = read("VERSION"),
    author = "TEXTA",
    author_email = "info@texta.ee",
    description = ("texta-tools"),
    license = "GPLv3",
    packages = ["texta_tools"],
    data_files = ["VERSION", "requirements.txt", "README.md", "LICENSE"],
    long_description = read("README.md"),
    long_description_content_type="text/markdown",
    url="https://git.texta.ee/texta/texta-tools-python",
    install_requires = read("requirements.txt").split("\n"),
    include_package_data = True
)
