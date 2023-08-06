import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subfinder-vvvin",
    version="0.0.1",
    author="mian",
    author_email="wukuizongvincent@gmail.com",
    include_package_data=True,
    description="A Address Finder",
    install_requires=[
        "reverse_geocoder"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
