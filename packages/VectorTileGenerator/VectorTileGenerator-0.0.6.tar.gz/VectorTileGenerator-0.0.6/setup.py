import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VectorTileGenerator",
    version="0.0.6",
    description="Automatically generate a list of all possible tiles options between two zoom levels and a bounding box.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkeller3/VectorTileGenerator/",
    author="Michael Keller",
    author_email="michaelkeller03@gmail.com",
    license="GNU General Public License v3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        "console_scripts": [
            "VectorTileGenerator=VectorTileGenerator.__main__:main",
        ]
    },
)
