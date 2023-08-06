from setuptools import setup

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3"
]

with (open("README.md")) as f:
    long_description = f.read()

setup(
    name="blorbee-test-package",
    author="blorbee",
    author_email="truepoint000@gmail.com",
    version="1.0",
    description="test package",
    long_description=long_description,
    packages=["package"],
    include_package_data=True,
    classifiers=classifiers,
    python_requires=">=3.6"
)