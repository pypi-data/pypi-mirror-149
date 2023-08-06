import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-multi-stack-tfe",
    "version": "0.0.88",
    "description": "Sets up TFE / TFC workspaces for all stacks based on a seed stack.",
    "license": "MIT",
    "url": "https://github.com/DanielMSchmidt/cdktf-multi-stack-tfe.git",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schmidt<danielmschmidt92@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/DanielMSchmidt/cdktf-multi-stack-tfe.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_multi_stack_tfe",
        "cdktf_multi_stack_tfe._jsii"
    ],
    "package_data": {
        "cdktf_multi_stack_tfe._jsii": [
            "cdktf-multi-stack-tfe@0.0.88.jsii.tgz"
        ],
        "cdktf_multi_stack_tfe": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "cdktf-cdktf-provider-tfe>=0.2.0",
        "cdktf>=0.10.1, <0.11.0",
        "constructs>=10.0.107, <11.0.0",
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
