import setuptools


setuptools.setup(
    name="max6675",
    version="0.1",
    author="Francis B. Lavoie",
    author_email="francis.b.lavoie@usherbrooke.ca",
    description="MAX6675 thermocouple reading with pyfirmata2",
    long_description="MAX6675 thermocouple reading with pyfirmata2",
    long_description_content_type="text/markdown",
    url="https://catalyseur.ca/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ),
)