from setuptools import setup
from pgt import __version__ as pgt_version

with open("README.md") as f:
    long_desc = f.read()
print(pgt_version)
setup(
    name="tools-for-pygame",
    version=f"{pgt_version}",
    description="Tools to make using pygame easier",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Davide Taffarello - TheSilvered",
    packages=["pgt", "pgt.gui"],
    license="MIT",
    install_requres=["pygame>=2.0.0"],
    keywords=["pygame", "game", "video-game"],
    url="https://github.com/TheSilvered/pg-tools",
    download_url=f"https://github.com/TheSilvered/tools-for-pygame/archive/refs/tags/v{pgt_version}.tar.gz",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ]
)
