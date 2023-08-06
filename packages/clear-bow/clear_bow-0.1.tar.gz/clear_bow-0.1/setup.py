from setuptools import find_packages, setup

REQUIREMENTS = [
    "numpy>=1.22.2",
]

setup(
    name="clear_bow",
    version="0.1",
    url="https://github.com/samhardyhey/clear-bow",
    author="Sam Hardy",
    author_email="samhardyhey@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
)
