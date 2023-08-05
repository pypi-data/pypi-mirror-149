import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="singlejson",
    version="0.1",
    author="Qrashi",
    author_email="fritz@vibe.ac",
    description="A simple package providing easy to use JSON utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Qrashi/singlejson",
    license="GPL3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
