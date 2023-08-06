import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meteorpy",
    version="0.0.3",
    author="aerocyber",
    description="A tool to share python environment by building it from scratch on target machines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aerocyber/meteorpy/",
    project_urls={
        "Bug Tracker": "https://github.com/aerocyber/meteorpy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "meteorpy"},
    python_requires=">=3.6",
)
