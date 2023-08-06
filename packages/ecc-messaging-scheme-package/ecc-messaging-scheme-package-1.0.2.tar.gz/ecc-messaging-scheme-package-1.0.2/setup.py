import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ecc-messaging-scheme-package",
    version="1.0.2",
    description="ECCDH AES encryption/decryption Package",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ECC-Messaging/ECC-Messaging-Scheme-Package",
    author="Joe, Vibi",
    author_email="jmc529@vt.edu, vpeiris@vt.edu",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    include_package_data=True,
    install_requires=["tinyec", "AES"],
    entry_points={
        "console_scripts": [
            "ECCM=main.__main__:main",
        ]
    },
)
