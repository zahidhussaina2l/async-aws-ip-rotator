import pathlib
from setuptools import setup, find_packages

location = pathlib.Path(__file__).parent
README = (location / "README.md").read_text()

setup(
    name="async-aws-ip-rotator",
    version="1.0.2",
    description="Async IP rotation using AWS API Gateway with httpx support",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Zahid Hussain",
    author_email="zahidhussain.a2l@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "httpx>=0.24.0",
        "aioboto3>=11.0.0",
        "boto3",
        "botocore"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
