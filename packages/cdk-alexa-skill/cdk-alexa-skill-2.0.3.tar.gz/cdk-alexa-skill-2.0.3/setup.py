import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-alexa-skill",
    "version": "2.0.3",
    "description": "A construct library for deploying Alexa Skills with the AWS CDK.",
    "license": "MIT-0",
    "url": "https://github.com/aws-samples/cdk-alexa-skill",
    "long_description_content_type": "text/markdown",
    "author": "Jeff Gardner",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws-samples/cdk-alexa-skill"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_alexa_skill",
        "cdk_alexa_skill._jsii"
    ],
    "package_data": {
        "cdk_alexa_skill._jsii": [
            "cdk-alexa-skill@2.0.3.jsii.tgz"
        ],
        "cdk_alexa_skill": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
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
