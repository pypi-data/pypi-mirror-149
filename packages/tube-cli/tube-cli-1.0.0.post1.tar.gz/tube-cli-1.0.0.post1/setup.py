from setuptools import setup

with open("README.md", "r") as rd:
    long_description = rd.read()
setup(
    name="tube-cli",
    version="1.0.0-1",
    description="A command line tool that provides up-to-date status on the London Underground and various other TfL services",
    url="https://github.com/cxllm/tube-cli",
    author="Callum",
    author_email="hello@cxllm.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Freely Distributable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    keywords=["tfl", "london", "undergound", "tube"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["requests==2.27.1", "termcolor==1.1.0", "xmltodict==0.12.0"],
    scripts=["bin/underground"],
)
