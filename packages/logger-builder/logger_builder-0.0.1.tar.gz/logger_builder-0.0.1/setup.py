import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "logger_builder",
    version = "0.0.1",
    author = "Ludwik Bielczynski",
    author_email = "ludwik.bielczynski@gmail.com",
    description = "Logger builder to simplify creation of the loggers",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/LudwikBielczynski/logger_builder.git",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.6"
)