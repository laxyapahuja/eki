import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eki",
    version="0.0.7",
    author="Laxya Pahuja",
    author_email="laxya.pahuja8@gmail.com",
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
    entry_points={'console_scripts': ['eki=eki.__main__:main']},
    python_requires='>=3.6',
    install_requires=[
        'malupdate',
        'pywin32',
        'pymediainfo'
    ],
    project_urls={
        'Documentation': 'https://github.com/laxyapahuja/eki/README.md',
        'Source': 'https://github.com/laxyapahuja/eki'
    },
)
