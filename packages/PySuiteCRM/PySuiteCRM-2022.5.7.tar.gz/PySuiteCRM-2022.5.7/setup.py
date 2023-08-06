import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PySuiteCRM",
    version="2022.5.7",
    author="Russell Juma",
    author_email="RussellJuma@gmail.com",
    description="Python client for SuiteCRM v8 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RussellJuma/PySuiteCRM",
    project_urls={
        "Bug Tracker": "https://github.com/RussellJuma/PySuiteCRM/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)