import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bgdb",
    version="1.0.0",
    author="Nicholas Gleadall",
    author_email="ng384@cam.ac.uk",
    description="Python client for the BGDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ngleadall/bgdb_python_client",
    packages=setuptools.find_packages(),
    install_requires=["python-dotenv", "requests"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ),
)
