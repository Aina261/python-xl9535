from setuptools import setup, find_packages

setup(
    name="XL9535",
    version="0.1.0",
    description="A Python library for controlling the XL9535 I2C GPIO expander.",
    author="Aina261",
    author_email="contact@noarsoa.fr",
    url="https://github.com/Aina261/XL9535",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "smbus2"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 