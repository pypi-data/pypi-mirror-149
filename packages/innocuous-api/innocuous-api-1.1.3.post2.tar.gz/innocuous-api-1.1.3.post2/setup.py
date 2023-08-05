import os
import setuptools

_VERSION = "1.1.3-2"

DEPENDENCY_LINKS = [

]

REQUIRED_PACKAGES = [
    "colorlog",
    "halo",
    "pyjwt",
    "requests",
    "pyyaml"
]

setuptools.setup(
    name="innocuous-api",
    version=_VERSION,
    description="Innocuous Book API",
    install_requires=REQUIRED_PACKAGES,
    dependency_links=DEPENDENCY_LINKS,
    packages = ["innocuous_api"],
    zip_safe = False,
    author="noam",
    author_email="noamsrosenberg@gmail.com",
    url="",
    keywords=["innocuousbook"]
)
