from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="BoogieFN",
    version="1.0.3",
    description="BoogieFN Config",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/boogiefn",
    author="noteason",
    author_email="support@boogiefn.cf",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["BoogieFN"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "BoogieFN=boogiefn.cli:main",
        ]
    },
)