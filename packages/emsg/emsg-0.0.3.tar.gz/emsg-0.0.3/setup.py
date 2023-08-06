from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="emsg",
    version="0.0.3",
    description="An ISO BMFF emsg atom generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ygoto3/emsg",
    author="ygoto3",
    author_email="my.important.apes@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "emsg=emsg.cli.emsg:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={
        "Bug Reports": "https://github.com/ygoto3/emsg/issues",
        "Source": "https://github.com/ygoto3/emsg",
    },
)
