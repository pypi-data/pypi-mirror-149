from pathlib import Path
import setuptools


def load_description_from_file(file_name: str, long_description: str) -> str:
    try:
        if Path(file_name).is_file():
            with open(file_name, "r", encoding="utf-8") as fh:
                long_description = fh.read()
    except Exception as e:
        pass

    return long_description


long_description = ""
for description_file in ["README.md", "CHANGELOG.md"]:
    long_description = load_description_from_file(description_file, long_description)
    long_description += "/n/n"


setuptools.setup(
    name="logger_builder",
    version="0.0.2",
    author="Ludwik Bielczynski",
    author_email="ludwik.bielczynski@gmail.com",
    description="Logger builder to simplify creation of the loggers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LudwikBielczynski/logger_builder.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)
