import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eki", # Replace with your own username
    version="0.0.1",
    author="Laxya Pahuja",
    author_email="mail@laxya.co",
    description="MyAnimeList tracker for local anime files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laxyapahuja/eki",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)