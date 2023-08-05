from setuptools import setup, find_packages

setup(
    name="emsg",
    version="0.0.1",
    description="An ISO BMFF emsg atom generator",
    url="https://github.com/ygoto3/emsg",
    author="ygoto3",
    author_email="my.important.apes@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "emsg=emsg:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/ygoto3/emsg/issues",
        "Source": "https://github.com/ygoto3/emsg",
    },
)