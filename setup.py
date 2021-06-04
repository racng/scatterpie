import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scatterpie",
    version="0.0.1",
    author="Rachel Ng",
    author_email="rachelng323@gmail.com",
    description="Scatter pie charts in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/racng/scatterpie",
    packages=['scatterpie'],
    package_dir={'scatterpie':'scatterpie'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)