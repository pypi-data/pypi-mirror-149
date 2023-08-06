import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()
    
package_name = os.getenv(key="PACKAGE_NAME", default="arora")

setuptools.setup(
    name=package_name,
    version=os.getenv(key="PACKAGE_VERSION", default="0.1.1"),
    long_description=long_description,
    long_description_content="text/markdown",
    author="Sleep Revolution",
    author_email="sleeprevolution@ru.is",
    description="A tool for sleep researcher to preprocess, work, analyze and visualize data",
    packages=setuptools.find_packages("arora", "arora.*"),
    py_modules = ["find_features"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8"
        ],
    install_requires=["numpy", "pandas", "pyEDFlib", "scipy"],
    python_requires=">=3.8"
)
