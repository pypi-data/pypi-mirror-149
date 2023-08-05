import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-datalake-constructs",
    "version": "0.0.53",
    "description": "AWS CDK Constructs that can be used to create datalakes/meshes and more",
    "license": "MIT",
    "url": "https://github.com/randyridgley/cdk-datalake-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Randy Ridgley<randy.ridgley@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/randyridgley/cdk-datalake-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_datalake_constructs",
        "cdk_datalake_constructs._jsii"
    ],
    "package_data": {
        "cdk_datalake_constructs._jsii": [
            "cdk-datalake-constructs@0.0.53.jsii.tgz"
        ],
        "cdk_datalake_constructs": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.13.0, <3.0.0",
        "aws-cdk.aws-glue-alpha>=2.22.0.a0, <3.0.0",
        "aws-cdk.aws-lambda-python-alpha>=2.22.0.a0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.57.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
