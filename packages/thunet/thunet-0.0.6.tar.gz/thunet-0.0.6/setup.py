# flake8: noqa
from codecs import open

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

# with open("requirements.txt") as requirements:
#     REQUIREMENTS = [r.strip() for r in requirements if r != "\n"]

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/ShenDezhou/thunet/issues",
    "Documentation": "https://thunet.readthedocs.io/en/latest/",
    "Source": "https://github.com/ShenDezhou/thunet",
}

setup(
    name="thunet",
    version="0.0.6",
    author="Dezhou Shen",
    author_email="sdz15@tsinghua.org.cn",
    project_urls=PROJECT_URLS,
    url="https://github.com/ShenDezhou/thunet",
    description="A Deep learning framework for scientific and educational purpose",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy",
        "scipy"
    ],
    packages=find_packages(where='.', include=['*']),
    # package_dir={"": ""},
    license="GPLv3+",
    include_package_data=True,
    python_requires=">=2.7, >=3.0",
    extras_require={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
