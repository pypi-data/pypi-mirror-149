import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="flike-predict",
    short_description="Flike prediction API.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["flike"],
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "": ["*.so"],
    },
    version='1.0.1',
    license="MIT",
    python_requires=">=3",
    install_requires=[
        "certifi >= 2021.10.8",
        "charset-normalizer >= 2.0.12, <3",
        "idna >= 3.3, <4",
        "requests >= 2.27.1, <3",
        "urllib3 >= 1.26.9, <2"
    ],
    author_email='tech@flike.app',
)
