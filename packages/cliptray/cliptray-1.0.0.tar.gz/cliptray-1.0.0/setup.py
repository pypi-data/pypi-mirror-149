import pathlib
import cliptray
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cliptray",
    version=cliptray.__version__,
    description="A Tray icon tool allowing to quickly copy some values to the clipboard.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/McCzarny/cliptray",
    author="Maciej Czarnecki",
    author_email="mcczarny@gmail.com",
    license="The Unlicense",
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["cliptray"],
    include_package_data=True,
    install_requires=["pyperclip", "pystray"],
    entry_points={
        "console_scripts": [
            "cliptray=cliptray.__main__:main",
        ]
    },
)