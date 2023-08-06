import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

short_description = str("Python helper package for interacting with your Samourai Dojo instance")

setuptools.setup(
    name="dojo-py",
    version="0.0.4",
    author="Streets",
    author_email="streets@lofi.tools",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/streets/dojo-py",
    packages=["pydojo"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
