import pathlib

from setuptools import setup

README = (pathlib.Path(__file__).resolve().parent / "README.md").read_text()

setup(
    name="spanish-dni",
    version="1.0.1",
    description="Spanish DNI utilities for NIE/NIF",
    python_requires=">=3.8",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Joan Travé",
    author_email="jtravegordillo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["spanish_dni"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
    project_urls={
        "Source": "https://github.com/joanTrave/spanish_dni",
    }
)