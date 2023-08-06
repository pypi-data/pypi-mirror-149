import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyencoder",
    version="0.0.2",
    author="Simon Kojima",
    author_email="simon.kojima@outlook.com",
    description="encode and decode python list to string array",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simonkojima/pyencoder",
    project_urls={
        "Bug Tracker": "https://github.com/simonkojima/pyencoder/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)