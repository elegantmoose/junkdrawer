import pathlib
from setuptools import setup, find_packages


PARENT_DIR = pathlib.Path(__file__).parent
README = (PARENT_DIR / "README.md").read_text()

setup(
    name="junkdrawer",
    version="0.0.1",
    license="MIT",
    description="Useful Python utilities and patterns for a career Python developer.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/elegantmoose/junkdrawer",
    packages=find_packages(),
    install_requires=[
        "flask",
        "gunicorn",
        "pympler",
        "pytest",
        "pyyaml",
    ]
)
