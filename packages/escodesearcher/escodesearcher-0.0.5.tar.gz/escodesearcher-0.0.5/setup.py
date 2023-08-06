import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="escodesearcher",
    version="0.0.5",
    author="Mohamed Ashraf",
    author_email="Mohamed.ashraf881999@gmail.com",
    description="A source code searcher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/xTrimy/escodesearcher/issues",
        "Documentation": "https://github.com/xTrimy/escodesearcher/blob/master/README.md",
        'Source Code': 'https://github.com/xTrimy/escodesearcher/'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["tests","fetched_files"]),
    python_requires=">=3.6",
)
