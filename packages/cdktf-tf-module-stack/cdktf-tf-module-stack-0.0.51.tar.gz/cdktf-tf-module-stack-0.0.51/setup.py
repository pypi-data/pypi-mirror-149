import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-tf-module-stack",
    "version": "0.0.51",
    "description": "A drop-in replacement for cdktf.TerraformStack that let's you define Terraform modules as construct",
    "license": "Apache-2.0",
    "url": "https://github.com/DanielMSchmidt/cdktf-tf-module-stack.git",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schmidt<danielmschmidt92@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/DanielMSchmidt/cdktf-tf-module-stack.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_tf_module_stack",
        "cdktf_tf_module_stack._jsii"
    ],
    "package_data": {
        "cdktf_tf_module_stack._jsii": [
            "cdktf-tf-module-stack@0.0.51.jsii.tgz"
        ],
        "cdktf_tf_module_stack": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
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
