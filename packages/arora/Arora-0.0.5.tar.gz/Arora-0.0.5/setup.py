import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Arora",
    version=os.getenv(key="PACKAGE_VERSION", default="0.0.5"),
    long_description=long_description,
    long_description_content="text/markdown",
    author="Sleep Revolution",
    author_email="sleeprevolution@ru.is",
    description="A tool for sleep researcher to preprocess, work, analyze and visualize data",
    packages=setuptools.find_packages(include=['Arora', 'Arora.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8"
        ],
    install_requires=["numpy", "pandas", "pyEDFlib", "scipy"],
    python_requires=">=3.8"
)
