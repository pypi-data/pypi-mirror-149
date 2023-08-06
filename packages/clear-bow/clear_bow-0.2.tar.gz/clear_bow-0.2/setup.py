from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

REQUIREMENTS = [
    "numpy>=1.22.2",
]

setup(
    name="clear_bow",
    version="0.2",
    url="https://github.com/samhardyhey/clear-bow",
    author="Sam Hardy",
    author_email="samhardyhey@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
